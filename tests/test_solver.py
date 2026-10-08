import matplotlib

matplotlib.use("Agg")  # headless: no window needed

from patches.puzzle import load_puzzle  # noqa: E402
from patches.solver import solve  # noqa: E402
from patches.ui import PatchesApp  # noqa: E402

from test_rules import PROBLEM1_SOLUTION, SAMPLE_SOLUTION  # noqa: E402


def test_solve_problem1():
    puzzle = load_puzzle("puzzles/problem1.json")
    assert solve(puzzle) == PROBLEM1_SOLUTION


def test_solve_sample():
    puzzle = load_puzzle("puzzles/sample.json")
    assert solve(puzzle) == SAMPLE_SOLUTION


def test_hint_places_one_correct_region():
    app = PatchesApp(load_puzzle("puzzles/problem1.json"))
    app.on_key(type("Event", (), {"key": "h"})())
    assert len(app.board.regions) == 1
    (drone_id, rect), = app.board.regions.items()
    assert rect == PROBLEM1_SOLUTION[drone_id]
