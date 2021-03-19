#!/usr/bin/env python

import argparse
import math
import statistics as stat
import sys

def stats(cell_counts):
    return (stat.mean(cell_counts), stat.median(cell_counts), stat.mode(cell_counts), stat.variance(cell_counts))

def get_values(input):
    values = []
    for line in input:
        count = int(line.strip().split()[0])
        values.append(int(count))

    return values

def parse_args():
    parser = argparse.ArgumentParser(description='Generates stats.')
    parser.add_argument('-i', '--input', default=None, help="input file with values generating stats, one per line")
    parser.add_argument('-o', '--output', default=None, help="output file for stats")
    args = parser.parse_args()
    return args.input, args.output

def parse_from(file, parse_func, alt=sys.stdin):
    if file is not None:
        with open(file) as input:
            return parse_func(input)
    else:
        return parse_func(alt)

if __name__ == "__main__":
    input_file, output_file = parse_args()

    values = parse_from(input_file, get_values)

    mean, median, mode, variance = stats(values)

    output = f"Mean: {mean}\nMedian: {median}\nMode: {mode}\nVariance: {variance}\n"
    if output_file is None:
        print(output)
    else:
        with open(output_file, "w") as out:
            out.write(output)


