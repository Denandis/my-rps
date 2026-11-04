"""RPS-001 in a real browser: play one round, then replay a fresh one.

Uses the supplied live_server and page fixtures and real HTTP. Only the
computer's random move is fixed; the real rules decide each result. See SPEC.md.
"""

import pytest
from playwright.sync_api import Page, expect

import app as web

pytestmark = pytest.mark.e2e


def test_real_browser_round_and_replay(page: Page, live_server, monkeypatch):
    """Rock beats scissors (win); replaying Paper vs scissors loses."""
    # Fix only the computer's move; the real determine_winner decides results.
    monkeypatch.setattr(web.random, "choice", lambda _moves: "scissors")
    page.goto(live_server)

    # First round: player Rock vs computer Scissors -> player wins.
    page.get_by_role("button", name="Rock", exact=True).click()
    expect(page.get_by_label("This round’s choices")).to_be_visible()
    expect(page.get_by_text("You chose", exact=True)).to_be_visible()
    expect(page.get_by_text("Computer chose", exact=True)).to_be_visible()
    expect(page.locator("[data-outcome='win']")).to_be_visible()
    expect(page.get_by_role("heading", name="You win!")).to_be_visible()

    # Replay: choosing again starts an independent round with the real rules.
    page.get_by_role("button", name="Paper", exact=True).click()
    # Paper vs Scissors -> player loses.
    expect(page.locator("[data-outcome='lose']")).to_be_visible()
    expect(page.get_by_role("heading", name="Computer wins")).to_be_visible()
