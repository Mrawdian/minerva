"""
Fetching data from the Gitee API.

Works in anonymous mode. Handles:
- self-imposed rate limit: 50 requests/hour max + 2 s between requests
- 403 (Baidu WAF BDWAF): wait 60 s + one retry
- 404: returns None cleanly
"""

import logging
import threading
import time
from collections import deque

import requests

log = logging.getLogger("minerva.fetcher")

API_BASE = "https://gitee.com/api/v5"
RAW_BASE = "https://gitee.com"
USER_AGENT = "Minerva/0.1 (tech watch bot)"

MAX_REQUESTS_PER_HOUR = 50
DELAY_BETWEEN_REQUESTS_S = 2.0
WAF_RETRY_WAIT_S = 60.0
REQUEST_TIMEOUT_S = 30


_session = requests.Session()
_session.headers.update({"User-Agent": USER_AGENT})

# Sliding window of request timestamps to enforce the hourly quota.
# Protected by _rate_lock to allow parallel usage (ThreadPoolExecutor).
_request_timestamps: deque[float] = deque()
_rate_lock = threading.Lock()

# Gitee token (None = anonymous mode). Updated via configure().
_token: str | None = None


def configure(token: str | None) -> None:
    """Configure the client: token + adapted rate limit.

    - With token: 4500 req/h (Gitee limit 5000 - margin), 0.1 s between requests
      (parallelism-compatible — the hourly cap is enough to avoid the ban).
    - Without token: 50 req/h, 2 s between requests (anti-WAF, parallelism discouraged).
    """
    global _token, MAX_REQUESTS_PER_HOUR, DELAY_BETWEEN_REQUESTS_S
    _token = token or None
    if _token:
        MAX_REQUESTS_PER_HOUR = 4500
        DELAY_BETWEEN_REQUESTS_S = 0.1
    else:
        MAX_REQUESTS_PER_HOUR = 50
        DELAY_BETWEEN_REQUESTS_S = 2.0


def _acquire_rate_permit() -> None:
    """Blocks until a new request can be made, then reserves the slot.

    Combines "check capacity → sleep if needed → append timestamp" under a single lock,
    to prevent two threads from exceeding the hourly cap by crossing between check
    and reserve.
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
                time.sleep(wait)
                now = time.monotonic()

        if _request_timestamps:
            elapsed = now - _request_timestamps[-1]
            if elapsed < DELAY_BETWEEN_REQUESTS_S:
                time.sleep(DELAY_BETWEEN_REQUESTS_S - elapsed)
                now = time.monotonic()

        _request_timestamps.append(now)


def _get(url: str, params: dict | None = None) -> tuple[int | None, requests.Response | None]:
    """GET with rate limit, single retry on 403 WAF.

    Returns:
        (status_code, Response) if an HTTP response is received (Response = None if non-200).
        (None, None) if network error.
    """
    last_status: int | None = None
    effective_params = params
    if _token and "/api/v5/" in url:
        effective_params = dict(params or {})
        effective_params.setdefault("access_token", _token)

    for attempt in range(2):
        _acquire_rate_permit()

        try:
            r = _session.get(url, params=effective_params, timeout=REQUEST_TIMEOUT_S)
        except requests.RequestException:
            return None, None

        last_status = r.status_code
        if r.status_code == 200:
            return r.status_code, r
        if r.status_code == 404:
            return r.status_code, None
        if r.status_code == 403 and attempt == 0:
            # Baidu WAF: wait and retry once
            time.sleep(WAF_RETRY_WAIT_S)
            continue
        # persistent 403, 429, 5xx, etc.
        return r.status_code, None

    return last_status, None


def fetch_repo(owner: str, repo: str) -> dict | None:
    """Fetches the metadata of a Gitee repo.

    Returns:
        JSON dict from the API, or None if 404 or failure.
    """
    url = f"{API_BASE}/repos/{owner}/{repo}"
    _status, r = _get(url)
    if r is None:
        return None
    try:
        return r.json()
    except ValueError:
        return None


def _fetch_raw(owner: str, repo: str, branch: str, filename: str) -> str | None:
    """Fetches the raw content of a file from /{owner}/{repo}/raw/{branch}/{filename}."""
    url = f"{RAW_BASE}/{owner}/{repo}/raw/{branch}/{filename}"
    _status, r = _get(url)
    if r is None:
        return None
    content = r.text
    if len(content.strip()) < 20:
        return None
    return content


def search_repos(keyword: str, token: str, per_page: int = 50) -> list[dict]:
    """Searches for repos by keyword via /search/repositories.

    ⚠️  BROKEN ON THE GITEE SIDE — confirmed across 9 variants (probe_gitee_search.py):
      - q=rt-thread (current form)                → HTTP 200, 0 results
      - q + Authorization header instead of param → HTTP 200, 0 results
      - /search/repos (without -itories)          → HTTP 200, 0 results
      - + sort=stars_count + order=desc           → HTTP 200, 0 results
      - + language=C                              → HTTP 200, 0 results
      - + fork=true                               → HTTP 200, 0 results
      - POST instead of GET                       → HTTP 405 (method not supported)
      - q=rtthread (without hyphen)               → HTTP 200, 0 results
      - q=嵌入式 (Chinese keyword)                → HTTP 200, 0 results
      - q=ncnn (known repo name)                  → HTTP 200, 0 results

    /search/users works with the same token (sanity check) → it is indeed a
    server bug specific to /search/repositories, not an auth problem.

    Kept in place in case Gitee fixes it. To be used via _search_keywords
    which handles the clean skip on the pipeline side.
    """
    if not token:
        return []
    url = f"{API_BASE}/search/repositories"
    params = {"q": keyword, "access_token": token, "per_page": per_page}
    status, r = _get(url, params=params)
    if r is None:
        if status is not None:
            log.warning(f"Recherche '{keyword}' échouée (HTTP {status})")
        return []
    try:
        data = r.json()
    except ValueError:
        return []
    return data if isinstance(data, list) else []


def fetch_readme(owner: str, repo: str, branch: str = "master") -> str | None:
    """Fetches the raw README of the repo.

    Tries in order: README.md, README.rst, readme.md, README_CN.md.
    """
    for name in ("README.md", "README.rst", "readme.md", "README_CN.md"):
        content = _fetch_raw(owner, repo, branch, name)
        if content is not None:
            return content
    return None


def fetch_readme_en(owner: str, repo: str, branch: str = "master") -> str | None:
    """Fetches the English variant of the README for bilingual repos.

    Tries in order: README_EN.md, README.en.md, readme_en.md.
    """
    for name in ("README_EN.md", "README.en.md", "readme_en.md"):
        content = _fetch_raw(owner, repo, branch, name)
        if content is not None:
            return content
    return None


def _list_repos_by_owner_with_status(
    owner: str, page: int = 1, per_page: int = 100
) -> tuple[int | None, list[dict]]:
    """Identical to list_repos_by_owner but also returns the final HTTP code.

    The returned code is that of the last endpoint tried (orgs then users).
    """
    params = {"page": page, "per_page": per_page}
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


def list_repos_by_owner(owner: str, page: int = 1, per_page: int = 100) -> list[dict]:
    """Paginated list of the public repos of an account/organization.

    Tries /orgs/{owner}/repos then /users/{owner}/repos: most monitored Gitee
    accounts are organizations, but some individual profiles are only accessible
    via /users.

    Returns:
        list of repo JSON, or [] if failure on both endpoints.
    """
    _status, data = _list_repos_by_owner_with_status(owner, page=page, per_page=per_page)
    return data


class FetchPaginationError(Exception):
    """Raised if paginated enumeration fails with partial data already collected.

    Allows the orchestrator to distinguish 'genuinely empty account' from
    'incompletely enumerated account', and thus to avoid false deletion detections
    in the diff vs the previous run.
    """

    def __init__(self, owner: str, page: int, partial_count: int, status: int | None):
        self.owner = owner
        self.page = page
        self.partial_count = partial_count
        self.status = status
        super().__init__(
            f"[{owner}] Pagination échouée page {page} (HTTP {status}) "
            f"après retries — {partial_count} repos collectés avant l'échec"
        )


def list_all_repos_by_owner(owner: str, page_retries: int = 3) -> list[dict]:
    """Fetches all repos of an account by paginating automatically.

    Behavior in the face of intermediate errors (Gitee glitches):
      - On empty batch + non-200 status, retry up to `page_retries` times with
        exponential backoff (2s, 4s, 8s).
      - If all retries fail AND at least 1 page has already been collected: raise
        FetchPaginationError to signal partial data. The orchestrator can then
        ignore this owner for deletion detection.
      - If the first page itself fails: returns [] (normal behavior).

    Logs:
      - 404: account not found
      - 500: Gitee server error
      - 200 empty: account with no public repository
      - 200 + N repos: N repos found
    """
    per_page = 100
    all_repos: list[dict] = []
    page = 1
    last_status: int | None = None

    while True:
        # Try the current page with retries in case of intermediate failure
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
            all_repos.extend(batch)
            if len(batch) < per_page:
                break  # clean end of pagination
            page += 1
            continue

        # empty batch
        if page_status == 200:
            break  # legitimate end (empty page after the data)

        # persistent error after retries
        if all_repos:
            # partial data already collected → explicit signal
            raise FetchPaginationError(owner, page, len(all_repos), page_status)
        # Zero collected: a hard error on page 1 is a FETCH FAILURE, not an
        # empty account. Raise so the pipeline marks the owner as failed and
        # protects its repos from false deletion (post-mortem 2026-08-03: bad
        # CI credentials → 401 on every owner → the whole corpus was about to
        # be diffed away as "deleted"). Only 404 (account really gone) and 200
        # (genuinely empty) are treated as real absences.
        if page_status not in (200, 404):
            raise FetchPaginationError(owner, page, 0, page_status)
        break

    if all_repos:
        log.info(f"[{owner}] {len(all_repos)} repos trouvés (HTTP {last_status})")
    elif last_status == 404:
        log.warning(f"[{owner}] Compte introuvable (HTTP 404)")
    elif last_status == 500:
        log.warning(f"[{owner}] Erreur serveur Gitee (HTTP 500)")
    elif last_status == 403:
        log.warning(f"[{owner}] Accès refusé / WAF (HTTP 403)")
    elif last_status == 200:
        log.info(f"[{owner}] Compte sans dépôt public (HTTP 200, liste vide)")
    elif last_status is None:
        log.warning(f"[{owner}] Erreur réseau, aucune réponse HTTP")
    else:
        log.warning(f"[{owner}] Aucun repo (HTTP {last_status})")
    return all_repos


if __name__ == "__main__":
    repo = fetch_repo("mirrors", "rt-thread")
    print(f"Test fetch_repo: {'OK' if repo else 'FAIL'}")
    if repo:
        print(f"  full_name: {repo.get('full_name')}")
        print(f"  stars: {repo.get('stargazers_count')}")
