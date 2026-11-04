"""RPS-001 rules: nine literal outcomes plus one real request/result round.

The unit cases call determine_winner directly. The integration case sends a
real HTTP request through the supplied Flask shell, fixing only the computer's
random move so the real rules decide a repeatable result. See SPEC.md.
"""

import pytest

import app as web
import game


@pytest.mark.unit
@pytest.mark.parametrize(
    ("player", "computer", "expected"),
    [
        ("rock", "rock", "tie"),
        ("rock", "paper", "lose"),
        ("rock", "scissors", "win"),
        ("paper", "rock", "win"),
        ("paper", "paper", "tie"),
        ("paper", "scissors", "lose"),
        ("scissors", "rock", "lose"),
        ("scissors", "paper", "win"),
        ("scissors", "scissors", "tie"),
    ],
)
def test_determine_winner_matches_spec(player, computer, expected):
    """Each of the nine literal matchups returns the SPEC.md outcome."""
    assert game.determine_winner(player, computer) == expected


@pytest.mark.integration
def test_round_uses_real_rules_and_shows_both_choices(monkeypatch):
    """A posted round calls the real rules and displays both moves and result."""
    web.app.config.update(TESTING=True)
    client = web.app.test_client()
    # Fix only the randomness; the real determine_winner decides the outcome.
    monkeypatch.setattr(web.random, "choice", lambda _moves: "scissors")
    response = client.post("/", data={"move": "rock"})
    page = response.get_data(as_text=True)
    assert response.status_code == 200
    # Rock vs scissors is a win for the player, via the real rule function.
    assert 'data-outcome="win"' in page
    assert "You win!" in page
    assert "You chose" in page and "Computer chose" in page
    assert "Rock" in page and "Scissors" in page
