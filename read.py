import numpy as np
import re
import json

from typing import Tuple, Dict
from abc import ABC

class TileReplacementReader(ABC):
    def read_input_file(self, filename : str) -> Tuple[np.ndarray, Dict[str, int], Dict[int, int]]:

        with open(filename, "r") as file:
            lines = [line.replace('\n', '') for line in file.readlines()]

        landscape = []
        targets = dict()

        i = 0

        while not lines[i].startswith("# Landscape"):
            i += 1
        
        i += 1

        while lines[i]:
            pattern = r'(.)(?:.)?'

            landscape.append(
                [0 if matched == ' ' else int(matched) for matched in re.findall(pattern, lines[i])]
            )
            i += 1
        
        while not lines[i].startswith('# Tiles'):
            i += 1

        i += 1

        _tiles_extracted = re.sub(r'(\w+)=', r'"\1" : ', lines[i])
        tiles = json.loads(_tiles_extracted)

        while not lines[i].startswith('# Targets'):
            i += 1

        i += 1

        while i < len(lines) and lines[i]:
            pattern = r'(\d+):(\d+)'
            targets.update({
                int(st) : int(end) for st, end in re.findall(pattern, lines[i])
            })

            i += 1
        
        return np.array(landscape), tiles, targets