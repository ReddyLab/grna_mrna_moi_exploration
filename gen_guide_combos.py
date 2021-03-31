#!/usr/bin/env python

import argparse
import io
import itertools
import math
import sys

def get_grna_sets(input, umi_filter):
    temp_cell_ids = {}
    cell_ids = []

    is_comment = True
    for line in input:
        if line[0] == '%':
            continue

        if is_comment:
            # skip header
            is_comment = False
            continue

        entry = line.strip().split()

        grna_id = int(entry[0])
        cell_id = int(entry[1])
        umi_count = int(entry[2])
        if umi_count >= umi_filter:
            cell_subjects = temp_cell_ids.get(cell_id, set())
            cell_subjects.add(grna_id)
            temp_cell_ids[cell_id] = cell_subjects

    # filter out all cells with only 1 grna/mrna
    for k in temp_cell_ids:
        if len(temp_cell_ids[k]) >= 2:
            cell_ids.append((k, temp_cell_ids[k]))

    return cell_ids

def grna_set_combinations(grna_sets, combo_size):
    grna_set_len = len(grna_sets)
    for i, set in enumerate(grna_sets):
        for j in range(i+1, grna_set_len):
            cell_1 = grna_sets[i][0]
            set_1 = grna_sets[i][1]
            cell_2 = grna_sets[j][0]
            set_2 = grna_sets[j][1]
            intersection = set_1 & set_2
            for combo in itertools.combinations(intersection, combo_size):
                if len(combo) != combo_size:
                    continue
                yield (combo_size, cell_1, cell_2, combo)

def parse_args():
    parser = argparse.ArgumentParser(description='Generates a file of all shared gRNA combos of a given size between all cells.')
    parser.add_argument('-i', '--input', default=None, help="Input MatrixMarket file")
    parser.add_argument('-o', '--output', default=None, help="Output file with four datums: 1) combo size 2) cell id 1 3) cell id 2 4) subject combo")
    parser.add_argument('-f', '--umifilter', default=5, type=int, help="minimum umi count to include per gRNA/cell")
    parser.add_argument('-k', '--combosize', default=2, type=int, help="size of combinations to output")
    args = parser.parse_args()
    return args.input, args.output, args.umifilter, args.combosize

if __name__ == "__main__":
    input_file, output_file, umi_filter, combo_size = parse_args()

    if input_file is not None:
        with open(input_file) as input:
            grna_sets = get_grna_sets(input, umi_filter)
    else:
        grna_sets = get_grna_sets(sys.stdin, umi_filter)

    if output_file is None:
        out = sys.stdout
    else:
        out = open(output_file, "w")

    with io.StringIO() as output_buffer:
        lines = 0
        cell_1 = -1000
        for combo in grna_set_combinations(grna_sets, combo_size):
            cell = combo[1]
            if cell > cell_1 + 1000:
                if output_file is not None:
                    print(cell)
                cell_1 = cell
            output_buffer.write(f"{combo[0]} {cell} {combo[2]} {combo[3]}\n")
            lines += 1
            if lines == 10_000:
                out.write(output_buffer.getvalue())
                lines = 0
                output_buffer.seek(0)
                output_buffer.truncate()

        out.write(output_buffer.getvalue())

    if output_file is not None:
        out.close()
