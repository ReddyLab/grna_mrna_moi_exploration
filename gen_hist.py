#!/usr/bin/env python

import argparse
import math
import sys
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

def plot(values, max_value, bin_count, title='', x_label='', y_label='', density=False):
    fig, ax = plt.subplots()

    # the histogram of the data
    _n, _bins, _patches = ax.hist(values, bin_count, density=density)

    # plot MOI probability
    # bins = range(20)
    # moi = 7
    # y = [(moi**bin * np.e**-moi) / math.factorial(round(bin)) for bin in bins]

    # ax.plot(bins, y, '--')

    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_title(title)

    # create x-axis ticks
    step = max(int(round(max_value/10, -1)), 1) # 10 nice steps
    ticks = range(0, max_value, step)
    ax.set_xticks(ticks)

    # Tweak spacing to prevent clipping of ylabel
    fig.tight_layout()

    return fig

def get_values(input):
    values = []
    max_value = 0
    for line in input:
        value = int(line.strip().split()[0])
        values.append(value)
        if value > max_value:
            max_value = value

    return (values, max_value)

def parse_args():
    parser = argparse.ArgumentParser(description='Generate a histogram.')
    parser.add_argument('-i', '--input', default=None, help="input file with values for the histogram, one per line")
    parser.add_argument('-o', '--output', default=None, help="output file for histogram image")
    parser.add_argument('-b', '--bincount', type=int, default=100, help="number of bins for the histogram")
    parser.add_argument('-t', '--title', default='', help="histogram title")
    parser.add_argument('-x', '--xlabel', default='', help="label for the x-axis")
    parser.add_argument('-y', '--ylabel', default='', help="label for the y-axis")
    parser.add_argument('-d', '--density', action='store_const', const=True, default=False, help="show density values instead of counts on y-axis")
    args = parser.parse_args()
    return args.input, args.output, args.bincount, args.title, args.xlabel, args.ylabel, args.density

def parse_from(file, parse_func, alt=sys.stdin):
    if file is not None:
        with open(file) as input:
            return parse_func(input)
    else:
        return parse_func(alt)

if __name__ == "__main__":
    input_file, output_file, bin_count, title, x_label, y_label, density = parse_args()

    values, max_value = parse_from(input_file, get_values)

    fig = plot(values, max_value, bin_count, title=title, x_label=x_label, y_label=y_label, density=density)

    if output_file is None:
        plt.show()
    else:
        fig.savefig(output_file, transparent=False, dpi=80, bbox_inches="tight")
