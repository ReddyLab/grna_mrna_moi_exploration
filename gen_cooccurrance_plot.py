#!/usr/bin/env python

import argparse
import collections
import math
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

def plot(x_values, y_values, size_values, title='', x_label='', y_label=''):
    title = title.replace("\\n", "\n")

    fig, ax = plt.subplots()

    ax.scatter(x_values, y_values, s=size_values, cmap="flag")

    ax.set(xlabel=x_label, ylabel=y_label, title=title)

    # create x-axis ticks
    # step = int(round(max_value/10, -1)) # 10 nice steps
    # ticks = range(0, max_value, step)
    # ax.set_xticks(ticks)

    # Tweak spacing to prevent clipping of ylabel
    fig.tight_layout()

    return fig


def get_values(input):
    guide_pairs = []
    counts = []
    for line in input:
        combo, count, _cells = line.strip().split(maxsplit=2)
        grna1, grna2 = combo.strip('()').split(',')
        grna1 = int(grna1)
        grna2 = int(grna2)
        count = int(count)
        counts.append(count)
        guide_pairs.append((grna1, grna2))

    return guide_pairs, np.array(counts)

def parse_args():
    parser = argparse.ArgumentParser(description='Generate a plot of cell grna combination data.')
    parser.add_argument('-i', '--input', default=None, help="input file generated by gen_cells_per_guide_combo.py")
    parser.add_argument('-g', '--guidemapping', default=None, required=True, help="file with guide id -> guide information mapping")
    parser.add_argument('-o', '--output', default=None, help="output file for plot image")
    parser.add_argument('-p', '--paircount', type=int, default=755069, help="total number of guide pairs")
    parser.add_argument('-t', '--title', default='', help="plot title")
    parser.add_argument('-x', '--xlabel', default='', help="label for the x-axis")
    parser.add_argument('-y', '--ylabel', default='', help="label for the y-axis")
    args = parser.parse_args()
    return args.input, args.guidemapping, args.output, args.paircount, args.title, args.xlabel, args.ylabel

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
    input_file, guidemapping_file, output_file, pair_count, title, x_label, y_label = parse_args()

    guides = parse_guides(guidemapping_file)

    guide_pairs, counts = parse_from(input_file, get_values)

    scaled_counts = counts / pair_count

    pair_distances = []
    for g1, g2 in guide_pairs:
        guide1 = guides.get(g1, False)
        guide2 = guides.get(g2, False)
        if guide1 and guide2:
            pair_distances.append(guide1.dist(guide2))
        else:
            pair_distances.append(np.nan)

    pair_distances = np.array(pair_distances)
    nan_indices = np.where(np.isnan(pair_distances) == True)
    pair_distances = np.delete(pair_distances, nan_indices)
    scaled_counts = np.delete(scaled_counts, nan_indices)

    fig = plot(scaled_counts, pair_distances, [1 for _ in scaled_counts], title=title, x_label="pair cell count / total # pairs", y_label="chromosomal distance")

    if output_file is None:
        plt.show()
    else:
        fig.savefig(output_file, transparent=False, dpi=80, bbox_inches="tight")
