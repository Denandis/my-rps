"""RPS-001: the rules students will build with AI. See SPEC.md."""

# Each move beats exactly one other move. If the computer played the move the
# player's move beats, the player wins; equal moves tie; everything else loses.
BEATS = {"rock": "scissors", "paper": "rock", "scissors": "paper"}


def determine_winner(player: str, computer: str) -> str:
    """Return 'win', 'lose', or 'tie' from the player's perspective.

    The supplied web page accepts only 'rock', 'paper', and 'scissors'.
    See the expected results table in SPEC.md.
    """
    if player == computer:
        return "tie"
    if BEATS[player] == computer:
        return "win"
    return "lose"
