#!/usr/bin/env python
"""
Input:
  input: A file with a list of all the guides in each cell, organized by cell.
  guidemapping: a file that connects guide ids to the actual guide sequence.
Output:
  A set of files, one per "target" edit distance, with all the edit distances of
  the guide pairs in the cells that contain that "target" edit distance.
"""

import argparse
import itertools
import sys
import numpy as np
import matplotlib.pyplot as plt

from functools import lru_cache

class Guide:
    BASE_COMP_TABLE = str.maketrans('ATCG', 'TAGC')

    def __init__(self, chrom: str, start: int , end: int, strand: str, bases: str):
        self.chrom = chrom
        self.start = start
        self.end = end
        self.strand = strand
        self.bases = bases
        self.location = round((self.end + self.start) / 2)

    def dist(self, guide):
        if self.location > guide.location:
            return self.location - guide.location

        return guide.location - self.location

    def edit_dist(self, guide):
        return self._lev(self.bases, guide.bases)

    def rev_compliment_edit_dist(self, guide):
        guide_rev_comp = guide.bases[::-1].translate(Guide.BASE_COMP_TABLE)
        return self._lev(self.bases, guide_rev_comp)

    def min_edit_dist(self, guide):
        return min(self.edit_dist(guide), self.rev_compliment_edit_dist(guide))

    @lru_cache
    def _lev(self, a, b):
        if len(a) == 0: return len(b)
        if len(b) == 0: return len(a)
        if a[0] == b[0]: return self._lev(a[1:], b[1:])

        return 1 + min(
            self._lev(a, b[1:]),
            self._lev(a[1:], b),
            self._lev(a[1:], b[1:])
        )

def get_values(input):
    guide_pairs = []
    for line in input:
        line_segments = line.strip().split()
        pairs = line_segments[2:]
        guide_set = {int(pair.strip('()').split(',')[0]) for pair in pairs}
        guide_pairs.append(list(itertools.combinations(guide_set, 2)))

    return guide_pairs

def parse_args():
    parser = argparse.ArgumentParser(description='Generate histogram data from cell grna combination data.')
    parser.add_argument('-i', '--input', default=None, help="input file generated by gen_guide_read_per_cell.py")
    parser.add_argument('-g', '--guidemapping', default=None, required=True, help="file with guide id -> guide information mapping")
    parser.add_argument('-o', '--output', required=True, help="output file for histogram data")

    args = parser.parse_args()
    return args.input, args.guidemapping, args.output

def parse_guides(guidefile):
    guides = {}
    with open(guidefile) as guide_lines:
        for guide_line in guide_lines:
            line, guide = guide_line.split(' ', maxsplit=1)
            line = int(line)
            if not guide.startswith('chr'):
                continue
            guide_data = guide.split('-')
            if len(guide_data) == 6:
                guide_data[3] = '-'
                del guide_data[4]
            chrom, start, end, strand, bases = guide_data
            start = int(start)
            end = int(end)
            guides[line] = Guide(chrom, start, end, strand, bases)
    return guides

def parse_from(file, parse_func, alt=sys.stdin):
    if file is not None:
        with open(file) as input:
            return parse_func(input)
    else:
        return parse_func(alt)

if __name__ == "__main__":
    input_file, guidemapping_file, output_file = parse_args()

    guides = parse_guides(guidemapping_file)

    guide_pairs = parse_from(input_file, get_values)

    distances_0 = []
    distances_1 = []
    distances_2 = []
    distances_3 = []
    distances_4 = []
    distances_5 = []
    distances_6 = []

    for cell_pairs in guide_pairs:
        pair_distances = []
        for g1, g2 in cell_pairs:
            guide1 = guides.get(g1, False)
            guide2 = guides.get(g2, False)
            if guide1 and guide2:
                dist = guide1.min_edit_dist(guide2)
                pair_distances.append(dist)
        if 0 in pair_distances:
            distances_0.extend(pair_distances)
        if 1 in pair_distances:
            distances_1.extend(pair_distances)
        if 2 in pair_distances:
            distances_2.extend(pair_distances)
        if 3 in pair_distances:
            distances_3.extend(pair_distances)
        if 4 in pair_distances:
            distances_4.extend(pair_distances)
        if 5 in pair_distances:
            distances_5.extend(pair_distances)
        if 6 in pair_distances:
            distances_6.extend(pair_distances)

    with open(f"{output_file}_0", "w") as output:
        for number in distances_0:
            output.write(f"{number}\n")
    with open(f"{output_file}_1", "w") as output:
        for number in distances_1:
            output.write(f"{number}\n")
    with open(f"{output_file}_2", "w") as output:
        for number in distances_2:
            output.write(f"{number}\n")
    with open(f"{output_file}_3", "w") as output:
        for number in distances_3:
            output.write(f"{number}\n")
    with open(f"{output_file}_4", "w") as output:
        for number in distances_4:
            output.write(f"{number}\n")
    with open(f"{output_file}_5", "w") as output:
        for number in distances_5:
            output.write(f"{number}\n")
    with open(f"{output_file}_6", "w") as output:
        for number in distances_6:
            output.write(f"{number}\n")

