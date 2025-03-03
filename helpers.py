import numpy as np

from abc import ABC
from copy import deepcopy
from typing import Dict, Tuple

class TileReplacementHelper(ABC):
    """
    A helper class for managing tile replacement in a landscape grid.
    It provides methods to check tile placement validity, count digits, and manipulate the grid.
    """

    def can_put_tile(self, tile_name: str, landscape: np.ndarray[np.ndarray], X: int, Y: int) -> bool:
        """
        Checks if a tile can be placed at a given position without violating target constraints.

        :param tile_name: The name of the tile to place.
        :param landscape: The current landscape grid (NumPy 2D array).
        :param X: The x-coordinate (row index) for tile placement.
        :param Y: The y-coordinate (column index) for tile placement.
        :return: True if the tile can be placed, False otherwise.
        """
        # Create a copy of the landscape with the tile placed
        possible_landscape = self.put_tile(tile_name, landscape, X, Y)
        
        # Count the occurrences of each digit in the new landscape
        digits = self.count_occurences(possible_landscape)

        # Ensure that after placement, the required number of each digit is met
        for i in range(1, 5):
            if digits.get(i, 0) < self.targets.get(i, 0):  # If any digit count is less than required
                return False

        return True

    def is_found(self, landscape: np.ndarray[np.ndarray], targets: Dict[int, int]) -> bool:
        """
        Checks if the current landscape matches the target digit counts.

        :param landscape: The current landscape grid.
        :param targets: The expected count of each digit.
        :return: True if the landscape meets the target exactly, False otherwise.
        """
        digits = self.count_occurences(landscape)
        cnt = 0

        # Count how many digits have exactly the required number of tiles
        for i in range(1, 5):
            if digits.get(i) == targets.get(i):
                cnt += 1

        return cnt == 4  # Return True if all 4 target conditions are met

    def count_occurences(self, landscape: np.ndarray[np.ndarray]) -> Dict[int, int]:
        """
        Counts the occurrences of each digit in the landscape.

        :param landscape: The landscape grid.
        :return: A dictionary mapping each digit to its count.
        """
        result = {}

        # Iterate over all grid cells and count occurrences of each value
        for row in landscape:
            for value in row:
                result[value] = result.get(value, 0) + 1  # Increment count

        return result

    def get_next_location(self, landscape: np.ndarray[np.ndarray], locX: int, locY: int) -> Tuple[int, int]:
        """
        Determines the next location to check for tile placement.

        :param landscape: The landscape grid.
        :param locX: Current x-coordinate.
        :param locY: Current y-coordinate.
        :return: The next (X, Y) position, or (-1, -1) if no more positions exist.
        """
        # Move right by 4 units if within bounds
        if locX + 4 < len(landscape):
            locX += 4
        else:
            # Move down by 4 units if within bounds, resetting X to 0
            if locY + 4 < len(landscape[0]):
                locX = 0
                locY += 4
            else:
                return -1, -1  # No more valid positions

        return locX, locY

    def cover(self, row: np.ndarray, method: str) -> None:
        """
        Modifies a row by marking certain positions as covered (-1) based on the specified method.

        :param row: A row of the landscape grid.
        :param method: The method of covering ("full", "start", or "both").
        """
        if method == "full":
            # Mark the entire row as covered
            for i in range(len(row)):
                row[i] = -1

        elif method == "start":
            # Mark only the first cell in the row as covered
            row[0] = -1

        elif method == "both":
            # Mark the first and last cells in the row as covered
            row[0] = -1
            row[3] = -1

    def put_tile(self, tile_name: str, landscape: np.ndarray[np.ndarray], X: int, Y: int) -> np.ndarray:
        """
        Places a tile of the given type in the landscape at (X, Y).

        :param tile_name: The name of the tile to place.
        :param landscape: The landscape grid.
        :param X: The x-coordinate (row index).
        :param Y: The y-coordinate (column index).
        :return: A new landscape grid with the tile placed.
        """
        # Create a deep copy of the landscape to avoid modifying the original
        copy_landscape = deepcopy(landscape)

        # Extract 4x4 tile area from the landscape
        rows = copy_landscape[X:X+4]
        row1 = rows[0][Y:Y+4]
        row2 = rows[1][Y:Y+4]
        row3 = rows[2][Y:Y+4]
        row4 = rows[3][Y:Y+4]

        # Apply different tile shapes based on the type of tile
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

        return copy_landscape  # Return the modified landscape