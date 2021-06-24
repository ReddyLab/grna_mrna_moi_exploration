#!/usr/bin/env python

import argparse
import sys
import numpy as np
import matplotlib.pyplot as plt

from Guide import Guide, parse_guides

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
    parser.add_argument('-x', '--x-label', default='pair cell count / total # pairs', help="label for the x-axis")
    parser.add_argument('-y', '--y-label', default='genomic coordinate midpoint difference', help="label for the y-axis")
    distance_methods = parser.add_mutually_exclusive_group()
    distance_methods.add_argument('--chrom-dist', dest='dist_method', action='store_const',
                    const='dist', default='dist', help='measure distance by chromosomal distance')
    distance_methods.add_argument('--edit-dist', dest='dist_method', action='store_const',
                    const='edit_dist', help='measure distance by Levenshtein distance')
    distance_methods.add_argument('--rev-edit-dist', dest='dist_method', action='store_const',
                    const='rev_compliment_edit_dist', help='measure distance by Levenshtein distance of reverse compliment')
    distance_methods.add_argument('--min-edit-dist', dest='dist_method', action='store_const',
                    const='min_edit_dist', help='measure distance by minimum of 1) Levenshtein distance and 2) Levenshtein distance of reverse compliment')

    args = parser.parse_args()
    return args.input, args.guidemapping, args.output, args.paircount, args.title, args.x_label, args.y_label, args.dist_method

def parse_from(file, parse_func, alt=sys.stdin):
    if file is not None:
        with open(file) as input:
            return parse_func(input)
    else:
        return parse_func(alt)

if __name__ == "__main__":
    input_file, guidemapping_file, output_file, pair_count, title, x_label, y_label, dist_method = parse_args()

    guides = parse_guides(guidemapping_file)

    guide_pairs, counts = parse_from(input_file, get_values)

    scaled_counts = counts / pair_count

    pair_distances = []
    for g1, g2 in guide_pairs:
        guide1 = guides.get(g1, False)
        guide2 = guides.get(g2, False)
        if guide1 and guide2:
            dist = getattr(guide1, dist_method)(guide2)
            pair_distances.append(dist)
        else:
            pair_distances.append(np.nan)

    pair_distances = np.array(pair_distances)
    nan_indices = np.where(np.isnan(pair_distances) == True)
    pair_distances = np.delete(pair_distances, nan_indices)
    scaled_counts = np.delete(scaled_counts, nan_indices)

    fig = plot(scaled_counts, pair_distances, [1 for _ in scaled_counts], title=title, x_label=x_label, y_label=y_label)

    if output_file is None:
        plt.show()
    else:
        fig.savefig(output_file, transparent=False, dpi=80, bbox_inches="tight")