import numpy as np
from abc import ABC
from copy import deepcopy

from typing import Dict, Tuple

class TileReplacementHelper(ABC):
    def can_put_tile(self, tile_name : str, landscape : np.ndarray[np.ndarray], X : int, Y : int) -> bool:
        possible_landscape = self.put_tile(tile_name, landscape, X, Y)
        colors = self.count_colors(possible_landscape)

        for i in range(1, 5):
            if colors.get(i, 0) < self.targets.get(i, 0):
                return False

        return True
    
    def is_found(self, landscape : np.ndarray[np.ndarray], targets : Dict[int, int]) -> bool:
        colors = self.count_colors(landscape)
        cnt = 0

        for i in range(1, 5):
            if colors.get(i) == targets.get(i):
                cnt += 1

        return cnt == 4
    
    def count_colors(self, landscape : np.ndarray[np.ndarray]) -> Dict[int, int]:
        result = {}

        for row in landscape:
            for value in row:
                result[value] = result.get(value, 0) + 1

        return result

    def get_next_location(self, landscape : np.ndarray[np.ndarray], locX : int, locY : int) -> Tuple[int, int]:
        if locX + 4 < len(landscape):
            locX += 4
        else:
            if locY + 4 < len(landscape[0]):
                locX = 0
                locY += 4
            else:
                return -1, -1

        return locX, locY
    
    def cover(self, row : np.ndarray, method : str) -> None:
        if method == "full":
            for i in range(len(row)):
                row[i] = -1

        elif method == "start":
            row[0] = -1

        elif method == "both":
            row[0] = -1
            row[3] = -1

    def put_tile(self, tile_name : str, landscape : np.ndarray[np.ndarray], X : int, Y : int) -> np.ndarray:
        copy_landscape = deepcopy(landscape)

        rows = copy_landscape[X:X+4]
        row1 = rows[0][Y:Y+4]
        row2 = rows[1][Y:Y+4]
        row3 = rows[2][Y:Y+4]
        row4 = rows[3][Y:Y+4]

        if tile_name == "OUTER_BOUNDARY":
            self.cover(row1, "full")
            self.cover(row2, "both")
            self.cover(row3, "both")
            self.cover(row4, "full")

        elif tile_name == "EL_SHAPE":
            self.cover(row1, "full")
            self.cover(row2, "start")
            self.cover(row3, "start")
            self.cover(row4, "start")

        elif tile_name == "FULL_BLOCK":
            self.cover(row1, "full")
            self.cover(row2, "full")
            self.cover(row3, "full")
            self.cover(row4, "full")

        return copy_landscape