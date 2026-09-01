"""state-of-tic-tac-toe-fn-gamestate-conformance-oracle -- deterministic CONFORMANCE oracle for `state-of-tic-tac-toe` (python).

WHAT THIS DECIDES: given a candidate callable and one canonical input, it decides whether the candidate
agrees with the proven reference. It is a *conformance* decider over a fixed, published corpus -- it does
not decide correctness in general, and it says nothing about inputs outside the corpus.

SCOPE (declared, so the boundary is visible rather than discovered): the corpus is the canonical Exercism
test data for this task, 14 input/output pairs, listed in `probes/probes.jsonl`. Inputs outside that
set are simply not covered; `decide` answers only about the input it is given.

PARTIAL: the reference raises on 2 of the canonical inputs (input validation); those cases are recorded in `probes/known_limitations.jsonl` and are NOT part of the gate.

PROVENANCE: the reference body comes from the Exercism reference solution for `state-of-tic-tac-toe` (MIT, Exercism);
the type annotations were added by harvest, the body is unchanged (checked at AST level). The capability
was PROVEN by the exercism testsuite (pin=6f912fc7e6e88ee2) and re-executed by harvest in a sealed sandbox
(unshare -rn) -- verify-not-relay, not a copied ledger label.
"""

TASK = "state-of-tic-tac-toe"
CWE = "state-of-tic-tac-toe"          # a publish-motor egyseges mezonevet var; itt a feladat azonositoja


def decide(fn, value, expect):
    """PASS iff fn(value) == expect. Determinista, nincs halozat, nincs allapot."""
    try:
        return "PASS" if fn(value) == expect else "FAIL"
    except Exception:                                      # noqa: BLE001
        return "FAIL"


def gamestate(board: list) -> str:

    def check_if_won(player):
        for row in board:
            if all((cell == player for cell in row)):
                return True
        for col in range(3):
            if all((board[row][col] == player for row in range(3))):
                return True
        if all((board[i][i] == player for i in range(3))):
            return True
        if all((board[i][2 - i] == player for i in range(3))):
            return True
        return False
    x_count = sum((row.count('X') for row in board))
    o_count = sum((row.count('O') for row in board))
    if o_count > x_count:
        raise ValueError('Wrong turn order: O started')
    if x_count > o_count + 1:
        raise ValueError('Wrong turn order: X went twice')
    x_won = check_if_won('X')
    o_won = check_if_won('O')
    if x_won and o_won:
        raise ValueError('Impossible board: game should have ended after the game was won')
    if x_won:
        if x_count == o_count:
            raise ValueError('Impossible board: game should have ended after the game was won')
        return 'win'
    if o_won:
        if x_count > o_count:
            raise ValueError('Impossible board: game should have ended after the game was won')
        return 'win'
    if x_count + o_count == 9:
        return 'draw'
    return 'ongoing'

REFERENCE = gamestate
