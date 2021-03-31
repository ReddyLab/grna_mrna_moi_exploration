#!/usr/bin/env python

import argparse
import io

import math
import statistics as stat
import sys

from functools import lru_cache

DISTANCE_THRESHOLD = 2
BASE_COMP_TABLE = str.maketrans('ATCG', 'TAGC')

# Calculate Levenshtein distance
@lru_cache
def lev(a, b):
    if len(a) == 0: return len(b)
    if len(b) == 0: return len(a)
    if a[0] == b[0]: return lev(a[1:], b[1:])

    return 1 + min(
        lev(a, b[1:]),
        lev(a[1:], b),
        lev(a[1:], b[1:])
    )

# comp_table = str.maketrans('ATCG', 'TAGC')
# a = 'CCGCTGACACCCTGAAGGCT'
# b = 'CGCTGACACCCTGAAGGCTG'#[::-1].translate(comp_table)
# print(lev(a, b))

def rev_comp(bases):
    return bases[::-1].translate(BASE_COMP_TABLE)

def filter_pairs(input, guide_lookup):
    keep_lines = []
    for line in input:
        guide_pair, _rest = line.split(maxsplit=1)
        grna_id1, grna_id2 = guide_pair.strip('()').split(',')
        lev_dist = lev(guide_lookup[grna_id1], guide_lookup[grna_id2])
        rev_comp_lev_dist = lev(guide_lookup[grna_id1], rev_comp(guide_lookup[grna_id2]))
        if lev_dist > DISTANCE_THRESHOLD and rev_comp_lev_dist > DISTANCE_THRESHOLD:
        # if lev_dist > DISTANCE_THRESHOLD and guide_lookup[grna_id1] != rev_comp(guide_lookup[grna_id2]):
            keep_lines.append(line)
    return keep_lines

def parse_args():
    parser = argparse.ArgumentParser(description='Generates cells per combination data.')
    parser.add_argument('-i', '--input', default=None, help="input file that is the output of gen_cells_per_guide_combo.py")
    parser.add_argument('-g', '--guides', required=True, help="input file with two columns: 1) guide id 2) guide")
    parser.add_argument('-o', '--output', default=None, help="output file")
    args = parser.parse_args()
    return args.input, args.guides, args.output

if __name__ == "__main__":
    input_file, guide_file, output_file = parse_args()

    guide_lookup = {} # k: guide id, v: guide bases
    with open(guide_file) as guide_lines:
        for line in guide_lines:
            guide_id, guide = line.split()
            bases = guide.split('-')[-1]
            guide_lookup[guide_id] = bases

    if input_file is not None:
        with open(input_file) as input:
            grna_sets = filter_pairs(input, guide_lookup)
    else:
        grna_sets = filter_pairs(sys.stdin, guide_lookup)

    if output_file is None:
        out = sys.stdout
    else:
        out = open(output_file, "w")

    with io.StringIO() as output_buffer:
        lines = 0
        for line in grna_sets:
            output_buffer.write(line)
            lines += 1
            if lines == 10_000:
                out.write(output_buffer.getvalue())
                lines = 0
                output_buffer.seek(0)
                output_buffer.truncate()

        out.write(output_buffer.getvalue())

    if output_file is not None:
        out.close()
