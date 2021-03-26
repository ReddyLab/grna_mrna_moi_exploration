#!/usr/bin/env python

import argparse
from dataclasses import dataclass, field
import io
import itertools
import math
import sys

@dataclass
class GuidePair:
    guides: tuple[int, int]
    primary_guide: int
    cell_ids: set[str] = field(default_factory=set)

    def __str__(self):
        return f"({self.guides[0]},{self.guides[1]}) {len(self.cell_ids)} {' '.join(sorted(self.cell_ids))})"

@dataclass
class Clump:
    primary_guide: int
    defining_set: set[int] = field(default_factory=set)
    guide_pairs: list[GuidePair] = field(default_factory=list)

    ## Edit these methods (belongs, add, fit) to change how clumping happens

    def belongs(self, guide_pair):
        return self.fit(guide_pair) > 0

    def add(self, guide_pair):
        self.defining_set |= guide_pair.cell_ids
        self.guide_pairs.append(guide_pair)

    def fit(self, guide_pair):
        return len(self.defining_set | guide_pair.cell_ids)

    def __str__(self):
        clump_string = None
        with io.StringIO() as clump_buffer:
            clump_buffer.write(f"## Clump! {len(self.guide_pairs)}\n")
            for guide_pair in self.guide_pairs:
                clump_buffer.write(f"{guide_pair}\n")
            clump_string = clump_buffer.getvalue()
        return clump_string

@dataclass
class Clumps:
    clumps: dict[int, list[Clump]] = field(default_factory=dict)

    def _add_to_clump(self, guide_pair):
        if guide_pair.primary_guide not in self.clumps:
            return False

        added = False
        best_clumps = []
        best_clump_fit = 0
        for clump in self.clumps[guide_pair.primary_guide]:
            if clump.belongs(guide_pair):
                fit = clump.fit(guide_pair)
                if fit > best_clump_fit:
                    best_clumps = [clump]
                    best_clump_fit = fit

                elif fit == best_clump_fit:
                    best_clumps.append(clump)
                added = True

        for clump in best_clumps:
            clump.add(guide_pair)
        return added

    def empty(self):
        return len(self.clumps) > 0

    def add_guide_pair(self, guide_pair):
        if not self._add_to_clump(guide_pair):
            clump_list = self.clumps.get(guide_pair.primary_guide, [])
            clump = Clump(primary_guide=guide_pair.primary_guide)
            clump.add(guide_pair)
            clump_list.append(clump)
            self.clumps[guide_pair.primary_guide] = clump_list

    def __iter__(self):
        for k in self.clumps:
            for clump in self.clumps[k]:
                yield clump

    def __str__(self):
        clump_count = 0
        for k in self.clumps:
            clump_count += len(self.clumps[k])
        return f"{clump_count} total clumps"

def get_clumps(grna_sets):
    clumps = Clumps()
    for line in grna_sets:
        pair, count, cell_ids = line.split(maxsplit=2)
        guide_1, guide_2 = pair.strip('()').split(',')
        cell_id_set = set(cell_ids.split())
        clumps.add_guide_pair(GuidePair((int(guide_1), int(guide_2)), int(guide_1), cell_id_set))
        clumps.add_guide_pair(GuidePair((int(guide_1), int(guide_2)), int(guide_2), cell_id_set))
    return clumps

def parse_args():
    parser = argparse.ArgumentParser(description='Processes output of guide_cells_per_guide_combo.py to find "clumps" of cells with the same guide')
    parser.add_argument('-i', '--input', default=None, help="Output from guide_cells_per_guide_combo.py ")
    parser.add_argument('-o', '--output', default=None, help="file with 3 datums: 1) guide pair 2) count of cells with pair 3) list of cells")
    args = parser.parse_args()
    return args.input, args.output

if __name__ == "__main__":
    input_file, output_file = parse_args()

    if input_file is not None:
        with open(input_file) as input:
            clumps = get_clumps(input)
    else:
        clumps = get_clumps(sys.stdin)

    if output_file is None:
        out = sys.stdout
    else:
        out = open(output_file, "w")

    for clump in clumps:
        out.write(str(clump))

    if output_file is not None:
        out.close()
