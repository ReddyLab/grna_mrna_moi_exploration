#!/usr/bin/env python

import argparse
import collections
from dataclasses import dataclass
import io
import math
import sys

@dataclass
class GuideUMIs:
    guide: int
    umi_count: int

    def __str__(self):
        return f"({self.guide},{self.umi_count})"

def get_counts(input, umi_filter):
    is_comment = True
    cells = {}
    for line in input:
        if line[0] == '%':
            continue

        if is_comment:
            # skips the first non-comment line, which is a header
            is_comment = False
            continue

        entry = line.strip().split()

        guide_id = int(entry[0])
        cell_id = int(entry[1])
        umi_count = int(entry[2])
        if umi_count >= umi_filter:
            guides = cells.get(cell_id, [])
            guides.append(GuideUMIs(guide_id, umi_count))
            cells[cell_id] = guides

    return cells

def parse_args():
    parser = argparse.ArgumentParser(description='Generates guide reads per cell counts.')
    parser.add_argument('-i', '--input', default=None, help="Input MatrixMarket file")
    parser.add_argument('-o', '--output', default=None, help="Output file with 3 sets of data: 1) cell id 2) guide count 3) list of (guide id,read count) pairs")
    parser.add_argument('-f', '--umifilter', default=5, type=int, help="minimum umi count to include per gRNA/cell")
    args = parser.parse_args()
    return args.input, args.output, args.umifilter

if __name__ == "__main__":
    input_file, output_file, umi_filter = parse_args()

    if input_file is not None:
        with open(input_file) as input:
            cells = get_counts(input, umi_filter)
    else:
        cells = get_counts(sys.stdin, umi_filter)

    with io.StringIO() as output_buffer:
        for k in cells:
            # count cell_id
            output_buffer.write(f"{k} {len(cells[k])} {' '.join(map(lambda x: str(x), cells[k]))}\n")
        output = output_buffer.getvalue()

    if output_file is None:
        print(output)
    else:
        with open(output_file, "w") as out:
            out.write(output)


