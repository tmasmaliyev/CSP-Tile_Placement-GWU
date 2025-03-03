import sys
import argparse

from helpers import TileReplacementHelper  # Helper functions for tile placement
from read import TileReplacementReader  # File reading functionality
from copy import deepcopy  # To create deep copies of lists and dictionaries
from typing import List, Tuple  # Type hinting for function parameters

# Increase recursion limit to handle deep recursive calls
sys.setrecursionlimit(100000)

class TileReplacementSolver(TileReplacementHelper, TileReplacementReader):
    """
    Solver class that inherits from TileReplacementHelper and TileReplacementReader.
    It attempts to solve the tile replacement problem using backtracking.
    """
    tileNames = ["OUTER_BOUNDARY", "EL_SHAPE", "FULL_BLOCK"]  # List of available tile types

    def __init__(self, filepath: str) -> None:
        """
        Initialize the solver by reading input data from a file.
        """
        self.landscape, self.tiles, self.targets = self.read_input_file(filepath)  # Read input data
        self.path = []  # Stores the sequence of placed tiles
        self.is_solved = False  # Flag to check if a solution has been found

    def solve(self) -> None:
        """
        Start solving the problem using backtracking.
        """
        self.backtrack(0, 0, [])

    def backtrack(self, locX: int, locY: int, path: List[Tuple[int, int, str]]) -> bool:
        """
        Recursive backtracking function to find a valid tile placement.
        """
        # If the target pattern is already achieved, store the solution path
        if self.is_found(self.landscape, self.targets):
            self.path = path
            self.is_solved = True

            return True

        # Try placing each tile type
        for tileName in self.tileNames:
            if self.tiles[tileName] == 0:
                continue  # Skip if no tiles of this type are left

            copy_landscape = deepcopy(self.landscape)  # Make a backup before modification

            # Check if the tile can be placed at the current location
            if self.can_put_tile(tileName, self.landscape, locX, locY):
                self.tiles[tileName] -= 1  # Use one tile
                self.landscape = self.put_tile(tileName, self.landscape, locX, locY)  # Place tile

                prevLocX, prevLocY = locX, locY  # Store previous location
                locX, locY = self.get_next_location(self.landscape, locX, locY)  # Get next placement position

                # If there are no more places to fill, check if the solution is found
                if locX == -1 and locY == -1:
                    if self.is_found(self.landscape, self.targets):
                        self.path = path
                        self.is_solved = True
                        return True
                
                # Recursively continue solving
                elif self.backtrack(locX, locY, path + [(prevLocX, prevLocY, tileName)]):
                    return True

                # Backtrack if placement was unsuccessful
                locX, locY = prevLocX, prevLocY
                self.landscape = deepcopy(copy_landscape)  # Restore landscape state
                self.tiles[tileName] += 1  # Restore tile count

        return False  # No valid placement found at this step

    def get_path(self) -> None:
        """
        Print the sequence of tile placements that led to the solution.
        """
        for x, y, tile in self.path:
            print(f'({x:2}, {y:2}) : {tile}')


def main(filepath: str) -> None:
    """
    Main function to initialize the solver and execute the tile replacement process.
    """
    solver = TileReplacementSolver(filepath)  # Initialize solver with file input
    solver.solve()  # Attempt to solve the problem

    if solver.is_solved:
        solver.get_path()  # Print the solution path
    else:
        print('There is no solution for this landscape!')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--filepath', 
                        type=str, required=True, 
                        help='Filepath of landscape, tile availability, and target as a .txt file')

    args = parser.parse_args()  # Parse arguments from command line
    main(args.filepath)  # Start main process