"""Backtracking solver: finds a full solution to a Patches puzzle."""

from .rules import Rect, is_solved, region_errors


def _candidate_rects(puzzle, drone):
    """Every rect on the grid containing the drone's own seed cell."""
    n = puzzle.grid_size
    row, col = drone.row, drone.col
    rects = []
    for top in range(row + 1):
        for height in range(row - top + 1, n - top + 1):
            for left in range(col + 1):
                for width in range(col - left + 1, n - left + 1):
                    rects.append(Rect(top, left, height, width))
    return rects


def solve(puzzle):
    """Backtracking search over the puzzle's drones.

    Returns the full solution as a dict {drone_id: Rect}, or None if no
    solution exists.
    """
    drones = puzzle.drones
    regions = {}

    def backtrack(index):
        if index == len(drones):
            return is_solved(puzzle, regions)
        drone = drones[index]
        for rect in _candidate_rects(puzzle, drone):
            if region_errors(puzzle, drone, rect):
                continue
            if any(rect.overlaps(r) for r in regions.values()):
                continue
            regions[drone.id] = rect
            if backtrack(index + 1):
                return True
            del regions[drone.id]
        return False

    if backtrack(0):
        return dict(regions)
    return None
