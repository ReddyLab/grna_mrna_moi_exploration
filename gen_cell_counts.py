#!/usr/bin/env python

import argparse
import collections
import io
import math
import sys

def get_counts(input, umi_filter):
    duped_cell_ids = []
    unique_cell_ids = set()
    total_cells = 0
    is_comment = True
    for line in input:
        if line[0] == '%':
            continue

        if is_comment:
            is_comment = False
            total_cells = int(line.strip().split()[1])
            continue

        entry = line.strip().split()

        cell_id = int(entry[1])
        umi_count = int(entry[2])
        if umi_count >= umi_filter:
            duped_cell_ids.append(cell_id)
            unique_cell_ids.add(cell_id)

    counter = collections.Counter(duped_cell_ids)
    for x in range(1, total_cells + 1):
        if x not in unique_cell_ids:
            counter[x] = 0
    return counter

def parse_args():
    parser = argparse.ArgumentParser(description='Generates cell counts.')
    parser.add_argument('-i', '--input', default=None, help="Input MatrixMarket file")
    parser.add_argument('-o', '--output', default=None, help="Output file with two columns: 1) cell count 2) cell id")
    parser.add_argument('-f', '--umifilter', default=5, type=int, help="minimum umi count to include per gRNA/cell")
    args = parser.parse_args()
    return args.input, args.output, args.umifilter

if __name__ == "__main__":
    input_file, output_file, umi_filter = parse_args()

    if input_file is not None:
        with open(input_file) as input:
            counter = get_counts(input, umi_filter)
    else:
        counter = get_counts(sys.stdin, umi_filter)

    with io.StringIO() as output_buffer:
        for k in counter:
            # count cell_id
            output_buffer.write(f"{counter[k]} {k}\n")
        output = output_buffer.getvalue()

    if output_file is None:
        print(output)
    else:
        with open(output_file, "w") as out:
            out.write(output)


