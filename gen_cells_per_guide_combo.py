#!/usr/bin/env python

import argparse
import io
import math
import statistics as stat
import sys

def get_combo_cells(input):
    values = {}
    for line in input:
        _count, cell1, cell2, combo = line.strip().split(maxsplit=3)
        grna_ids = combo.strip('()').split(', ')
        grna_ids = sorted(grna_ids)
        grna_combo_string =','.join(grna_ids)

        cell_set = values.get(grna_combo_string, set())
        cell_set.add(cell1)
        cell_set.add(cell2)
        values[grna_combo_string] = cell_set

    return values

def parse_args():
    parser = argparse.ArgumentParser(description='Generates cells per combination data.')
    parser.add_argument('-i', '--input', default=None, help="input file with cell and combo values")
    parser.add_argument('-o', '--output', default=None, help="output file for stats")
    args = parser.parse_args()
    return args.input, args.output

if __name__ == "__main__":
    input_file, output_file = parse_args()

    if input_file is not None:
        with open(input_file) as input:
            grna_sets = get_combo_cells(input)
    else:
        grna_sets = get_combo_cells(sys.stdin)

    if output_file is None:
        out = sys.stdout
    else:
        out = open(output_file, "a")

    with io.StringIO() as output_buffer:
        lines = 0
        for combo in grna_sets:
            cells = grna_sets[combo]
            output_buffer.write(f"({combo}) {len(cells)} {' '.join(cells)}\n")
            lines += 1
            if lines == 10_000:
                out.write(output_buffer.getvalue())
                lines = 0
                output_buffer.seek(0)
                output_buffer.truncate()

        out.write(output_buffer.getvalue())

    if output_file is not None:
        out.close()
