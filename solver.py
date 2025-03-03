import sys
import argparse

from helpers import TileReplacementHelper
from read import TileReplacementReader
from copy import deepcopy

from typing import List, Tuple

sys.setrecursionlimit(100000)

class TileReplacementSolver(TileReplacementHelper, TileReplacementReader):
    tileNames = ["OUTER_BOUNDARY", "EL_SHAPE", "FULL_BLOCK"]

    def __init__(self, filepath : str):
        self.landscape, self.tiles, self.targets = self.read_input_file(filepath)
        self.path = []
        self.is_solved = False

    def solve(self):
        self.backtrack(0, 0, [])

    def backtrack(self, locX : int, locY : int, path : List[Tuple[int, int, str]]) -> None:
        if self.is_found(self.landscape, self.targets):
            self.path = path
            self.is_solved = True

            return True

        for tileName in self.tileNames:
            if self.tiles[tileName] == 0:
                continue

            copy_landscape = deepcopy(self.landscape)

            if self.can_put_tile(tileName, self.landscape, locX, locY):
                self.tiles[tileName] -= 1

                self.landscape = self.put_tile(tileName, self.landscape, locX, locY)

                prevLocX, prevLocY = locX, locY
                locX, locY = self.get_next_location(self.landscape, locX, locY)

                if locX == -1 and locY == -1:
                    if self.is_found(self.landscape, self.targets):
                        self.path = path
                        self.is_solved = True

                        return True
                
                elif self.backtrack(locX, locY, path + [(prevLocX, prevLocY, tileName)]):
                    return True

                locX, locY = prevLocX, prevLocY

                self.landscape = deepcopy(copy_landscape)
                self.tiles[tileName] += 1

        return False

    def get_path(self):
        
        for x, y, tile in self.path:
            print(f'({x:2}, {y:2}) : {tile}')


def main(filepath : str):
    solver = TileReplacementSolver(filepath) 
    solver.solve()

    if solver.is_solved:
        solver.get_path()
    else:
        print('There is no solution for this landscape !')


if __name__ == '__main__':
    # Define Argument parser and add argument
    parser = argparse.ArgumentParser()
    parser.add_argument('--filepath', 
                        type=str, required=True, 
                        help='Filepath of landscape, how many tiles for each and target as .txt file'
    )

    # Parse arguments from command line
    args = parser.parse_args()

    # Start Main process
    main(args.filepath)