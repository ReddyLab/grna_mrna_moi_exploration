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
import sys

from Guide import parse_guides

def get_values(input):
    segments = []
    for line in input:
        line_segments = line.strip().split()
        pair = line_segments[0]
        g1, g2 = pair.strip('()').split(',')
        segments.append((int(g1), int(g2)))
    return segments

def gen_distances(guide_gen, guides):
    distances = []
    for g1, g2 in guide_gen:
        guide1 = guides.get(g1, False)
        guide2 = guides.get(g2, False)
        if guide1 and guide2:
            distances.append(guide1.min_edit_dist(guide2))
    return distances

def parse_args():
    parser = argparse.ArgumentParser(description='Generate histogram data from cell grna combination data.')
    parser.add_argument('-i', '--input', default=None, help="input file generated by gen_guide_read_per_cell.py")
    parser.add_argument('-g', '--guidemapping', default=None, required=True, help="file with guide id -> guide information mapping")
    parser.add_argument('-o', '--output', default=None, help="output file for histogram data")

    args = parser.parse_args()
    return args.input, args.guidemapping, args.output

def parse_from(file, parse_func, alt=sys.stdin):
    if file is not None:
        with open(file) as input:
            return parse_func(input)
    else:
        return parse_func(alt)

if __name__ == "__main__":
    input_file, guidemapping_file, output_file = parse_args()

    guides = parse_guides(guidemapping_file)

    if output_file is not None:
        with open(output_file) as output:
            for dist in gen_distances(parse_from(input_file, get_values), guides):
                output.write(f"{dist}\n")
    else:
        for dist in gen_distances(parse_from(input_file, get_values), guides):
            sys.stdout.write(f"{dist}\n")