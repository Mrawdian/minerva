"""Tests de src/fetcher.py — fetch_repo, list_repos_by_owner, gestion 200/404/403."""

from unittest.mock import MagicMock, patch

import fetcher


class FakeResponse:
    def __init__(self, status_code: int, json_data=None, text: str = ""):
        self.status_code = status_code
        self._json = json_data
        self.text = text

    def json(self):
        if self._json is None:
            raise ValueError("no json")
        return self._json


@patch.object(fetcher, "_session")
def test_fetch_repo_200_returns_dict(mock_session):
    mock_session.get.return_value = FakeResponse(200, json_data={"full_name": "owner/repo", "stargazers_count": 42})
    result = fetcher.fetch_repo("owner", "repo")
    assert result is not None
    assert result["full_name"] == "owner/repo"
    assert result["stargazers_count"] == 42


@patch.object(fetcher, "_session")
def test_fetch_repo_404_returns_none(mock_session):
    mock_session.get.return_value = FakeResponse(404)
    result = fetcher.fetch_repo("owner", "missing")
    assert result is None


@patch.object(fetcher, "_session")
@patch.object(fetcher, "WAF_RETRY_WAIT_S", 0)  # pas d'attente réelle pendant les tests
def test_fetch_repo_403_retries_then_fails(mock_session, *_):
    """403 WAF : doit retry une fois (selon la logique existante) puis abandonner."""
    mock_session.get.side_effect = [
        FakeResponse(403),
        FakeResponse(403),
    ]
    result = fetcher.fetch_repo("owner", "repo")
    assert result is None
    assert mock_session.get.call_count == 2


@patch.object(fetcher, "_session")
def test_fetch_repo_network_error_returns_none(mock_session):
    import requests
    mock_session.get.side_effect = requests.ConnectionError("network down")
    result = fetcher.fetch_repo("owner", "repo")
    assert result is None


@patch.object(fetcher, "_session")
def test_fetch_repo_invalid_json_returns_none(mock_session):
    mock_session.get.return_value = FakeResponse(200, json_data=None, text="not json")
    result = fetcher.fetch_repo("owner", "repo")
    assert result is None


@patch.object(fetcher, "_session")
def test_list_repos_by_owner_org_path(mock_session):
    """Path /orgs/{owner}/repos doit être tenté en premier."""
    mock_session.get.return_value = FakeResponse(200, json_data=[{"full_name": "owner/repo1"}])
    repos = fetcher.list_repos_by_owner("someorg", page=1, per_page=20)
    assert len(repos) == 1
    assert repos[0]["full_name"] == "owner/repo1"
    # Vérifier que l'URL contient /orgs/
    args, kwargs = mock_session.get.call_args
    assert "/orgs/someorg/repos" in args[0] or kwargs.get("url", "").endswith("/orgs/someorg/repos")


def test_configure_authenticated_sets_higher_rate():
    """Avec token : 4500 req/h, délai serré (compatible parallélisme).
    Sans token : 50 req/h, délai 2s (anti-WAF)."""
    fetcher.configure("fake-token")
    assert fetcher.MAX_REQUESTS_PER_HOUR == 4500
    assert fetcher.DELAY_BETWEEN_REQUESTS_S == 0.1

    fetcher.configure(None)
    assert fetcher.MAX_REQUESTS_PER_HOUR == 50
    assert fetcher.DELAY_BETWEEN_REQUESTS_S == 2.0


# ─── Post-mortem 2026-08-03 : un 401 page 1 = échec de fetch, pas un compte vide ───

@patch.object(fetcher.time, "sleep")
@patch.object(fetcher, "_session")
def test_list_repos_hard_error_page1_raises_not_empty(mock_session, mock_sleep):
    """Un 401 persistant dès la page 1 (zéro repo collecté) doit lever
    FetchPaginationError pour que le pipeline protège l'owner — pas retourner
    une liste vide (qui ferait passer tout le corpus de l'owner en 'supprimé')."""
    import pytest
    mock_session.get.return_value = FakeResponse(401)
    with pytest.raises(fetcher.FetchPaginationError):
        fetcher.list_all_repos_by_owner("someowner")


@patch.object(fetcher.time, "sleep")
@patch.object(fetcher, "_session")
def test_list_repos_404_still_returns_empty(mock_session, mock_sleep):
    """404 = compte réellement absent : liste vide légitime, pas d'exception."""
    mock_session.get.return_value = FakeResponse(404)
    assert fetcher.list_all_repos_by_owner("gone-owner") == []
