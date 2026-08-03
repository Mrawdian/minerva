"""
Fetching data from the GitHub API (REST v3).

Connector complementary to `fetcher.py` (Gitee) to capture the Chinese embedded /
IoT / robotics / edge-AI organizations that publish ONLY on GitHub
(Bouffalo Lab, Sophgo, Unitree, DeepRobotics, Canaan/Kendryte, Allwinner…),
listed as a blind spot in the README (Known limitations).

Contract: produces exactly the same repo dict schema as fetcher.py
(full_name, description, language, stargazers_count, forks_count, pushed_at,
default_branch, archived) to stay transparent towards analyzer and
translator. Each repo is tagged `_minerva_source="github"` so that the
pipeline routes the README fetch and the fiche URL to the right host.

Auth: `GITHUB_TOKEN` optional.
  - Without token: 60 requests/hour (anonymous GitHub limit) → enough for a
    smoke test, insufficient for a full multi-org run.
  - With token (PAT with scope `public_repo` or even empty/read-only): 5000 req/h.

Handles: self-imposed rate limit + respect of X-RateLimit-Remaining, clean 404,
403/429 (secondary rate limit) with wait + retry, automatic pagination.
"""

import logging
import threading
import time
from collections import deque

import requests

log = logging.getLogger("minerva.github_fetcher")

API_BASE = "https://api.github.com"
USER_AGENT = "Minerva/0.1 (tech watch bot)"
API_VERSION = "2022-11-28"

# Self-imposed rate limit. Recalibrated by configure() based on token presence.
MAX_REQUESTS_PER_HOUR = 55  # margin below the anonymous 60/h
DELAY_BETWEEN_REQUESTS_S = 1.0
SECONDARY_RATELIMIT_WAIT_S = 60.0
REQUEST_TIMEOUT_S = 30

# By default we discard pure forks (fork=True): they are almost always
# copies of upstream without original work, hence noise for the watch.
SKIP_FORKS = True

_session = requests.Session()
_session.headers.update({
    "User-Agent": USER_AGENT,
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": API_VERSION,
})

# Sliding window of timestamps to enforce the hourly quota (thread-safe).
_request_timestamps: deque[float] = deque()
_rate_lock = threading.Lock()

# GitHub token (None = anonymous). Updated via configure().
_token: str | None = None


class GitHubPaginationError(Exception):
    """Pagination interrupted by an error after already collecting ≥1 page.

    Mirror of fetcher.FetchPaginationError: signals PARTIAL data so that
    an owner is not falsely considered as "all deleted" in the diff vs the
    previous run.
    """

    def __init__(self, owner: str, page: int, partial_count: int, status: int | None):
        self.owner = owner
        self.page = page
        self.partial_count = partial_count
        self.status = status
        super().__init__(
            f"[{owner}] Pagination GitHub échouée page {page} (HTTP {status}) "
            f"après retries — {partial_count} repos collectés avant l'échec"
        )


def configure(token: str | None) -> None:
    """Configure the client: token + adapted rate limit.

    - With token: 4500 req/h (GitHub limit 5000 - margin), 0.1 s between requests.
    - Without token: 55 req/h (anonymous limit 60 - margin), 1 s between requests.
    """
    global _token, MAX_REQUESTS_PER_HOUR, DELAY_BETWEEN_REQUESTS_S
    _token = token or None
    if _token:
        _session.headers["Authorization"] = f"Bearer {_token}"
        MAX_REQUESTS_PER_HOUR = 4500
        DELAY_BETWEEN_REQUESTS_S = 0.1
    else:
        _session.headers.pop("Authorization", None)
        MAX_REQUESTS_PER_HOUR = 55
        DELAY_BETWEEN_REQUESTS_S = 1.0


def _acquire_rate_permit() -> None:
    """Blocks until a new request can be made, then reserves the slot.

    Identical in spirit to fetcher._acquire_rate_permit: check capacity → sleep →
    reserve, all under a single lock to prevent two threads from exceeding the
    hourly cap by crossing.
    """
    with _rate_lock:
        now = time.monotonic()
        hour_ago = now - 3600
        while _request_timestamps and _request_timestamps[0] < hour_ago:
            _request_timestamps.popleft()

        if len(_request_timestamps) >= MAX_REQUESTS_PER_HOUR:
            oldest = _request_timestamps[0]
            wait = (oldest + 3600) - now
            if wait > 0:
                log.warning(f"Quota horaire GitHub atteint — attente {wait:.0f}s")
                time.sleep(wait)
                now = time.monotonic()

        if _request_timestamps:
            elapsed = now - _request_timestamps[-1]
            if elapsed < DELAY_BETWEEN_REQUESTS_S:
                time.sleep(DELAY_BETWEEN_REQUESTS_S - elapsed)
                now = time.monotonic()

        _request_timestamps.append(now)


def _get(url: str, params: dict | None = None,
         accept: str | None = None) -> tuple[int | None, requests.Response | None]:
    """GET with rate limit + single retry on 403/429 (secondary rate limit).

    Returns:
        (status_code, Response) if HTTP 200.
        (status_code, None) for 404 / non-recoverable non-200 errors.
        (None, None) if network error.
    """
    headers = {"Accept": accept} if accept else None
    last_status: int | None = None

    for attempt in range(2):
        _acquire_rate_permit()
        try:
            r = _session.get(url, params=params, headers=headers,
                             timeout=REQUEST_TIMEOUT_S)
        except requests.RequestException:
            return None, None

        last_status = r.status_code
        if r.status_code == 200:
            return r.status_code, r
        if r.status_code == 404:
            return r.status_code, None

        # 403 (primary rate limit exhausted) or 429 (secondary rate limit).
        if r.status_code in (403, 429) and attempt == 0:
            remaining = r.headers.get("X-RateLimit-Remaining")
            if remaining == "0":
                reset = r.headers.get("X-RateLimit-Reset")
                wait = SECONDARY_RATELIMIT_WAIT_S
                if reset and reset.isdigit():
                    wait = max(0.0, min(300.0, int(reset) - time.time()))
                log.warning(f"Rate limit GitHub épuisé — attente {wait:.0f}s")
                time.sleep(wait)
            else:
                time.sleep(SECONDARY_RATELIMIT_WAIT_S)
            continue

        return r.status_code, None

    return last_status, None


def _normalize_repo(raw: dict) -> dict:
    """Projects a raw GitHub repo onto Minerva's repo dict schema.

    The GitHub keys (full_name, stargazers_count, forks_count, pushed_at,
    default_branch, archived, language, description) already coincide with those
    expected by analyzer/translator; we just extract the useful subset
    and add the source tag.
    """
    return {
        "full_name": raw.get("full_name") or "",
        "description": raw.get("description") or "",
        "language": raw.get("language") or "",
        "stargazers_count": raw.get("stargazers_count") or 0,
        "forks_count": raw.get("forks_count") or 0,
        "pushed_at": raw.get("pushed_at") or "",
        "default_branch": raw.get("default_branch") or "main",
        "archived": bool(raw.get("archived")),
        "html_url": raw.get("html_url") or "",
        "_minerva_source": "github",
    }


def fetch_repo(owner: str, repo: str) -> dict | None:
    """Fetches the metadata of a GitHub repo, normalized.

    Returns:
        normalized repo dict, or None if 404 / failure.
    """
    url = f"{API_BASE}/repos/{owner}/{repo}"
    _status, r = _get(url)
    if r is None:
        return None
    try:
        raw = r.json()
    except ValueError:
        return None
    if not isinstance(raw, dict):
        return None
    return _normalize_repo(raw)


def fetch_readme(owner: str, repo: str, branch: str | None = None) -> str | None:
    """Fetches the raw README via /repos/{owner}/{repo}/readme.

    The contents/readme endpoint automatically resolves the real file name
    (README.md, README.rst, README_zh.md…) and the default branch, so the
    `branch` parameter is not necessary (accepted for signature compatibility
    with fetcher.fetch_readme).
    """
    url = f"{API_BASE}/repos/{owner}/{repo}/readme"
    _status, r = _get(url, accept="application/vnd.github.raw+json")
    if r is None:
        return None
    content = r.text
    if len(content.strip()) < 20:
        return None
    return content


def _list_repos_by_owner_with_status(
    owner: str, page: int = 1, per_page: int = 100
) -> tuple[int | None, list[dict]]:
    """Raw paginated list of the public repos of an account/organization.

    Tries /orgs/{owner}/repos then /users/{owner}/repos (like fetcher on the
    Gitee side): some targets are orgs, others user accounts.
    Returns the HTTP code of the last endpoint tried + the raw list.
    """
    params = {"page": page, "per_page": per_page, "sort": "pushed"}
    last_status: int | None = None
    for path in ("orgs", "users"):
        url = f"{API_BASE}/{path}/{owner}/repos"
        status, r = _get(url, params=params)
        last_status = status
        if r is None:
            continue
        try:
            data = r.json()
        except ValueError:
            continue
        if isinstance(data, list):
            return status, data
    return last_status, []


def list_all_repos_by_owner(owner: str, page_retries: int = 3) -> list[dict]:
    """Fetches all repos of a GitHub account by paginating automatically.

    Same guarantees as fetcher.list_all_repos_by_owner:
      - retry with backoff on intermediate failure;
      - GitHubPaginationError if failure AFTER ≥1 page collected (partial
        data → the orchestrator protects the owner from deletion
        detection);
      - [] if the first page fails (account not found, etc.).

    Applies the SKIP_FORKS filter (discards pure forks) and normalizes each
    retained repo.
    """
    per_page = 100
    all_repos: list[dict] = []
    page = 1
    last_status: int | None = None
    skipped_forks = 0

    while True:
        batch: list[dict] = []
        page_status: int | None = None
        for attempt in range(page_retries):
            page_status, batch = _list_repos_by_owner_with_status(
                owner, page=page, per_page=per_page
            )
            if batch or page_status == 200:
                break
            if attempt < page_retries - 1:
                wait = 2 * (2 ** attempt)
                log.warning(
                    f"[{owner}] page {page} HTTP {page_status} — "
                    f"retry {attempt + 1}/{page_retries - 1} dans {wait}s"
                )
                time.sleep(wait)
        last_status = page_status

        if batch:
            for raw in batch:
                if SKIP_FORKS and raw.get("fork"):
                    skipped_forks += 1
                    continue
                all_repos.append(_normalize_repo(raw))
            if len(batch) < per_page:
                break  # clean end of pagination
            page += 1
            continue

        # empty batch
        if page_status == 200:
            break  # legitimate end
        if all_repos:
            raise GitHubPaginationError(owner, page, len(all_repos), page_status)
        # Zero collected + hard error on page 1 = fetch failure, not an empty
        # org — raise so the owner is protected from false deletion (mirror of
        # fetcher.py; post-mortem 2026-08-03). 404 stays a real absence.
        if page_status not in (200, 404):
            raise GitHubPaginationError(owner, page, 0, page_status)
        break

    if all_repos:
        extra = f", {skipped_forks} forks écartés" if skipped_forks else ""
        log.info(f"[{owner}] {len(all_repos)} repos GitHub retenus (HTTP {last_status}){extra}")
    elif last_status == 404:
        log.warning(f"[{owner}] Compte GitHub introuvable (HTTP 404)")
    elif last_status in (403, 429):
        log.warning(f"[{owner}] Rate limit / accès refusé GitHub (HTTP {last_status})")
    elif last_status == 200:
        log.info(f"[{owner}] Compte GitHub sans dépôt public (ou 100% forks)")
    elif last_status is None:
        log.warning(f"[{owner}] Erreur réseau GitHub, aucune réponse HTTP")
    else:
        log.warning(f"[{owner}] Aucun repo GitHub (HTTP {last_status})")
    return all_repos


if __name__ == "__main__":
    import os

    configure(os.environ.get("GITHUB_TOKEN"))
    repo = fetch_repo("kendryte", "nncase")
    print(f"Test fetch_repo: {'OK' if repo else 'FAIL'}")
    if repo:
        print(f"  full_name: {repo.get('full_name')}")
        print(f"  stars: {repo.get('stargazers_count')}")
        print(f"  source: {repo.get('_minerva_source')}")
