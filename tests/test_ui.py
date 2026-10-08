from types import SimpleNamespace

import matplotlib

matplotlib.use("Agg")  # headless: no window needed

from matplotlib.patches import Circle  # noqa: E402

from patches.puzzle import load_puzzle  # noqa: E402
from patches.ui import PatchesApp, format_time  # noqa: E402

from test_rules import PROBLEM1_SOLUTION  # noqa: E402


def make_app():
    return PatchesApp(load_puzzle("puzzles/problem1.json"))


def test_clues_shown_while_unsolved():
    app = make_app()
    assert len(app.ax.texts) == len(app.puzzle.drones)


def test_clues_become_drones_when_solved():
    app = make_app()
    for rect in PROBLEM1_SOLUTION.values():
        app.board.place(rect)
    app.redraw()
    assert len(app.ax.texts) == 0
    circles = [p for p in app.ax.patches if isinstance(p, Circle)]
    assert len(circles) == 5 * len(app.puzzle.drones)


def test_clues_return_after_unsolving():
    app = make_app()
    for rect in PROBLEM1_SOLUTION.values():
        app.board.place(rect)
    app.board.remove_at(0, 0)
    app.redraw()
    assert len(app.ax.texts) == len(app.puzzle.drones)


# ---- move counter and timer ------------------------------------------------

def mouse(app, button, row, col):
    """A fake Matplotlib mouse event over cell (row, col)."""
    return SimpleNamespace(button=button, inaxes=app.ax, xdata=col + 0.5, ydata=row + 0.5)


def drag(app, rect):
    """Left-drag from the top-left to the bottom-right cell of `rect`."""
    app.on_press(mouse(app, 1, rect.top, rect.left))
    app.on_release(mouse(app, 1, rect.top + rect.height - 1, rect.left + rect.width - 1))


def test_moves_start_at_zero_and_placement_adds_one():
    app = make_app()
    assert app.moves == 0
    drag(app, PROBLEM1_SOLUTION["drone_1"])
    assert app.moves == 1


def test_rejected_placement_is_not_a_move():
    app = make_app()
    app.on_press(mouse(app, 1, 1, 1))  # cell (1, 1) holds no seed
    app.on_release(mouse(app, 1, 1, 1))
    assert app.moves == 0


def test_right_click_removal_is_a_move_but_empty_cell_is_not():
    app = make_app()
    drag(app, PROBLEM1_SOLUTION["drone_1"])
    app.on_press(mouse(app, 3, 5, 5))  # nothing to remove here
    assert app.moves == 1
    app.on_press(mouse(app, 3, 0, 0))
    assert app.moves == 2


def test_reset_sets_moves_and_timer_back_to_zero():
    app = make_app()
    drag(app, PROBLEM1_SOLUTION["drone_1"])
    app.on_key(SimpleNamespace(key="r"))
    assert app.moves == 0
    assert app.elapsed() == 0


def test_format_time():
    assert format_time(0) == "0:00"
    assert format_time(65) == "1:05"
    assert format_time(600.9) == "10:00"


def test_timer_starts_at_first_move():
    app = make_app()
    now = [100]
    app.clock = lambda: now[0]
    now[0] = 130
    assert app.elapsed() == 0  # no move yet
    drag(app, PROBLEM1_SOLUTION["drone_1"])
    now[0] = 195
    assert app.elapsed() == 65
    assert "Moves: 1 · Time: 1:05" in app.stats_text()


def test_timer_stops_when_solved():
    app = make_app()
    now = [0]
    app.clock = lambda: now[0]
    for rect in PROBLEM1_SOLUTION.values():
        drag(app, rect)
        now[0] += 10
    # the last move happened at 70 seconds after the first
    now[0] = 500
    assert app.elapsed() == 70
    assert "SOLVED in 1:10 with 8 moves!" in app.ax.get_title()
