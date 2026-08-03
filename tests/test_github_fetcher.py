"""Tests de src/github_fetcher.py — normalisation, pagination, forks, rate-limit, README.

Réseau entièrement mocké (patch de github_fetcher._session). time.sleep est
neutralisé et la fenêtre de rate-limit remise à zéro avant chaque test pour
éviter toute attente réelle.
"""

from unittest.mock import patch

import pytest

import github_fetcher as gf


class FakeResponse:
    def __init__(self, status_code: int, json_data=None, text: str = "", headers=None):
        self.status_code = status_code
        self._json = json_data
        self.text = text
        self.headers = headers or {}

    def json(self):
        if self._json is None:
            raise ValueError("no json")
        return self._json


@pytest.fixture(autouse=True)
def _no_sleep_no_ratelimit():
    """Neutralise les attentes et repart d'une fenêtre de quota vide à chaque test."""
    gf._request_timestamps.clear()
    with patch.object(gf.time, "sleep", lambda *_: None):
        yield
    gf._request_timestamps.clear()


# ─── Normalisation ───────────────────────────────────────────────────────

def test_normalize_repo_maps_fields_and_tags_source():
    raw = {
        "full_name": "sophgo/tpu-mlir",
        "description": "TPU compiler",
        "language": "C++",
        "stargazers_count": 954,
        "forks_count": 120,
        "pushed_at": "2026-05-01T10:00:00Z",
        "default_branch": "master",
        "archived": False,
        "html_url": "https://github.com/sophgo/tpu-mlir",
        "fork": False,
    }
    n = gf._normalize_repo(raw)
    assert n["full_name"] == "sophgo/tpu-mlir"
    assert n["stargazers_count"] == 954
    assert n["forks_count"] == 120
    assert n["pushed_at"] == "2026-05-01T10:00:00Z"
    assert n["default_branch"] == "master"
    assert n["_minerva_source"] == "github"


def test_normalize_repo_defaults_for_missing_fields():
    n = gf._normalize_repo({"full_name": "owner/repo"})
    assert n["description"] == ""
    assert n["language"] == ""
    assert n["stargazers_count"] == 0
    assert n["forks_count"] == 0
    assert n["default_branch"] == "main"  # défaut GitHub
    assert n["archived"] is False
    assert n["_minerva_source"] == "github"


# ─── fetch_repo ──────────────────────────────────────────────────────────

@patch.object(gf, "_session")
def test_fetch_repo_200_returns_normalized(mock_session):
    mock_session.get.return_value = FakeResponse(
        200, json_data={"full_name": "kendryte/nncase", "stargazers_count": 898}
    )
    r = gf.fetch_repo("kendryte", "nncase")
    assert r is not None
    assert r["full_name"] == "kendryte/nncase"
    assert r["stargazers_count"] == 898
    assert r["_minerva_source"] == "github"


@patch.object(gf, "_session")
def test_fetch_repo_404_returns_none(mock_session):
    mock_session.get.return_value = FakeResponse(404)
    assert gf.fetch_repo("owner", "missing") is None


@patch.object(gf, "_session")
def test_fetch_repo_network_error_returns_none(mock_session):
    import requests
    mock_session.get.side_effect = requests.ConnectionError("down")
    assert gf.fetch_repo("owner", "repo") is None


# ─── fetch_readme ────────────────────────────────────────────────────────

@patch.object(gf, "_session")
def test_fetch_readme_returns_raw_text(mock_session):
    mock_session.get.return_value = FakeResponse(200, text="# Projet\nUn vrai README long.")
    out = gf.fetch_readme("owner", "repo")
    assert out is not None
    assert "Projet" in out


@patch.object(gf, "_session")
def test_fetch_readme_too_short_returns_none(mock_session):
    mock_session.get.return_value = FakeResponse(200, text="x")
    assert gf.fetch_readme("owner", "repo") is None


@patch.object(gf, "_session")
def test_fetch_readme_404_returns_none(mock_session):
    mock_session.get.return_value = FakeResponse(404)
    assert gf.fetch_readme("owner", "repo") is None


# ─── list_all_repos_by_owner ─────────────────────────────────────────────

@patch.object(gf, "_session")
def test_list_all_repos_skips_forks(mock_session):
    mock_session.get.return_value = FakeResponse(200, json_data=[
        {"full_name": "org/original", "fork": False},
        {"full_name": "org/aforked", "fork": True},
    ])
    repos = gf.list_all_repos_by_owner("org")
    names = [r["full_name"] for r in repos]
    assert "org/original" in names
    assert "org/aforked" not in names
    assert all(r["_minerva_source"] == "github" for r in repos)


@patch.object(gf, "_session")
def test_list_all_repos_paginates(mock_session):
    """Une page pleine (100) puis une page partielle → arrêt propre, tout collecté."""
    page1 = [{"full_name": f"org/repo{i}", "fork": False} for i in range(100)]
    page2 = [{"full_name": "org/last", "fork": False}]
    # orgs page1 (plein) → orgs page2 (partiel, arrêt)
    mock_session.get.side_effect = [
        FakeResponse(200, json_data=page1),
        FakeResponse(200, json_data=page2),
    ]
    repos = gf.list_all_repos_by_owner("org")
    assert len(repos) == 101
    assert repos[-1]["full_name"] == "org/last"


@patch.object(gf, "_session")
def test_list_all_repos_partial_then_fail_raises(mock_session):
    """Page 1 pleine OK, puis page 2 en échec persistant → GitHubPaginationError."""
    page1 = [{"full_name": f"org/repo{i}", "fork": False} for i in range(100)]
    # orgs p1 plein ; puis p2 : orgs 500 + users 500 × 3 retries → toujours vide
    responses = [FakeResponse(200, json_data=page1)]
    responses += [FakeResponse(500)] * 20  # de quoi couvrir tous les retries/paths
    mock_session.get.side_effect = responses
    with pytest.raises(gf.GitHubPaginationError) as exc:
        gf.list_all_repos_by_owner("org", page_retries=2)
    assert exc.value.partial_count == 100
    assert exc.value.owner == "org"


@patch.object(gf, "_session")
def test_list_all_repos_first_page_404_returns_empty(mock_session):
    mock_session.get.return_value = FakeResponse(404)
    assert gf.list_all_repos_by_owner("ghost", page_retries=1) == []


# ─── configure ───────────────────────────────────────────────────────────

def test_configure_authenticated_sets_header_and_rate():
    gf.configure("fake-pat")
    assert gf.MAX_REQUESTS_PER_HOUR == 4500
    assert gf.DELAY_BETWEEN_REQUESTS_S == 0.1
    assert gf._session.headers.get("Authorization") == "Bearer fake-pat"

    gf.configure(None)
    assert gf.MAX_REQUESTS_PER_HOUR == 55
    assert gf.DELAY_BETWEEN_REQUESTS_S == 1.0
    assert "Authorization" not in gf._session.headers
