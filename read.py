import numpy as np
import re
import json

from typing import Tuple, Dict
from abc import ABC

class TileReplacementReader(ABC):
    def read_input_file(self, filename: str) -> Tuple[np.ndarray, Dict[str, int], Dict[int, int]]:
        """
        Reads an input file and extracts:
        - Landscape as a NumPy array
        - Tiles as a dictionary (tile type -> count)
        - Targets as a dictionary (start value -> end value)

        :param filename: The name of the input file to read.
        :return: A tuple containing (landscape, tiles, targets).
        """

        # Open the file and read all lines, stripping newline characters
        with open(filename, "r") as file:
            lines = [line.replace('\n', '') for line in file.readlines()]

        landscape = []  # Stores the landscape grid
        targets = {}  # Stores the target mappings

        i = 0  # Line index tracker

        # Find the section that starts with "# Landscape"
        while not lines[i].startswith("# Landscape"):
            i += 1
        i += 1  # Move to the next line after the header

        # Parse the landscape grid
        while lines[i]:
            pattern = r'(.)(?:.)?'  # Regex to match each character (handling spaces correctly)

            # Convert the matched characters into a grid format
            # ' ' (space) becomes 0, digits remain as integers
            landscape.append(
                [0 if matched == ' ' else int(matched) for matched in re.findall(pattern, lines[i])]
            )
            i += 1  # Move to the next line

        # Find the section that starts with "# Tiles"
        while not lines[i].startswith("# Tiles"):
            i += 1
        i += 1  # Move to the next line after the header

        # Convert the tile information into a dictionary using regex and JSON parsing
        # Example: Converts "A=3, B=2" → { "A": 3, "B": 2 }
        _tiles_extracted = re.sub(r'(\w+)=', r'"\1" : ', lines[i])
        tiles = json.loads(_tiles_extracted)  # Convert string to dictionary

        # Find the section that starts with "# Targets"
        while not lines[i].startswith("# Targets"):
            i += 1
        i += 1  # Move to the next line after the header

        # Parse the target mappings
        while i < len(lines) and lines[i]:
            pattern = r'(\d+):(\d+)'  # Matches "start:end" patterns
            targets.update({
                int(st): int(end) for st, end in re.findall(pattern, lines[i])
            })
            i += 1  # Move to the next line

        # Return landscape as a NumPy array, along with tiles and targets as dictionaries
        return np.array(landscape), tiles, targets
