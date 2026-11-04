# Rock, Paper, Scissors

## RPS-001: Play a round

**Purpose:** one person plays a quick round against the computer.

- Choose rock, paper, or scissors. The computer chooses one move for that round.
- Display both choices and the result: **You win!**, **Computer wins**, or **It’s a tie**.
- Choosing again starts an independent round. No score or saved history.
- Keep the supplied interface and server. Name/color changes can wait until the rules work.

### Expected results

Results are from the **player’s perspective**. `determine_winner(player, computer)` in `game.py` returns `win`, `lose`, or `tie`. Inputs are the lowercase moves below; the supplied server rejects other choices.

| Player | Computer | Expected return |
| --- | --- | --- |
| rock | rock | tie |
| rock | paper | lose |
| rock | scissors | win |
| paper | rock | win |
| paper | paper | tie |
| paper | scissors | lose |
| scissors | rock | lose |
| scissors | paper | win |
| scissors | scissors | tie |

### Agreed plan

**Prediction:** Player Rock vs computer Scissors returns `win`, because rock smashes scissors from the player's perspective. This matches the expected results table above.

**Plan:** Implement `determine_winner(player, computer)` in `game.py` using a mapping of which move each move beats. Equal moves return `tie`; if the computer played the move the player's move beats, return `win`; otherwise `lose`. Keep the supplied server and interface unchanged.

**Valid losing round:** Player Paper vs computer Scissors returns `lose` (scissors cut paper).

**Rejected input:** A missing move or an unsupported value (for example `lizard` or an empty move) is rejected by the supplied server with HTTP 400 and the message "Choose Rock, Paper, or Scissors to play." before the rules run.

### Checks

Before coding, agree this small test plan with AI:

| Level | Cases and evidence |
| --- | --- |
| Unit — positive | All nine literal expected results above, including valid losses and ties. |
| Integration — positive | A submitted round uses the real rule function and displays both choices and the correct result. Fix the computer choice for the test. |
| Integration — negative | Reuse supplied missing/unsupported-move tests: HTTP 400 and a helpful explanation, without calling the rules. A crash is not the intended result. |
| E2E — positive | Add a real-browser round and replay in tests/e2e/test_round.py using the supplied live_server/page fixtures. Fix only the computer choice; use real rules and real HTTP. |

Use `unit`, `integration`, and `e2e` pytest markers. Run `.venv/bin/python check.py` for Black, Pylint, fast tests, and browser checks; then review the diff. Keep shared settings and meaningful assertions intact. The student still plays, inspects a rule and its test, and gives feedback. Browser automation does not establish every aspect of usability or application performance.

### Work record

- Issue: https://github.com/Denandis/my-rps/issues/1
- Pull request / CI: add actual URLs when they exist.
- Implementation: `determine_winner` is built in `game.py` using a move-beats-move mapping; the supplied server and interface are unchanged.
- Checks: `.venv/bin/python check.py` passes locally: Black, Pylint, pytest non-browser (nine unit cases, one integration round, and the reused missing/invalid-input checks), and the real Chromium browser round and replay.
- Played round: I chose Paper, the computer chose Rock, and the page showed "You win!" This is correct because paper covers rock. Each click started a fresh independent round, and Tab plus Enter played a round from the keyboard.
- Test explained: `test_determine_winner_matches_spec` asserts `determine_winner("rock", "scissors") == "win"`. If the rules returned the wrong result (for example `lose` when the player should win), this assertion would fail and catch the mistake.
- Files: `game.py`, `tests/test_game.py`, `tests/e2e/test_round.py`.
