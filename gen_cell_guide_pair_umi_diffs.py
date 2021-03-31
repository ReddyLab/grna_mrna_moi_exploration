#!/usr/bin/env python

import argparse
import io
import statistics as stat
import sys

def stats(cell_counts):
    return (stat.mean(cell_counts), stat.median(cell_counts), stat.mode(cell_counts), stat.variance(cell_counts))

def get_umi_ratios(input):
    umi_ratios = []
    umi_counts = []
    for line in input:
        _cell_id, _guide_count, guide_1, guide_2 = line.split()
        guide_1, guide_1_umi_count = guide_1.strip('()').split(',')
        guide_2, guide_2_umi_count = guide_2.strip('()').split(',')
        max_count = int(max(guide_1_umi_count, guide_2_umi_count))
        min_count = int(min(guide_1_umi_count, guide_2_umi_count))

        umi_ratios.append(min_count / max_count)
        umi_counts.append(max_count + min_count)

    return umi_ratios, umi_counts

def parse_args():
    parser = argparse.ArgumentParser(description='Generates information about umi differences in cells with two guides.')
    parser.add_argument('-i', '--input', default=None, help="Input of guides per cell where each cell has two guides\nThis is the output of gen_guide_read_per_cell.py filtered for 2 guides.")
    parser.add_argument('-o', '--output', default=None, help="Output file with two columns: 1) cell count 2) cell id")
    args = parser.parse_args()
    return args.input, args.output

if __name__ == "__main__":
    input_file, output_file = parse_args()

    if input_file is not None:
        with open(input_file) as input:
            umi_ratios, umi_counts = get_umi_ratios(input)
    else:
        umi_ratios, umi_counts = get_umi_ratios(sys.stdin)

    mean_r, median_r, mode_r, variance_r = stats(umi_ratios)
    mean_c, median_c, mode_c, variance_c = stats(umi_counts)

    with io.StringIO() as output_buffer:
        output_buffer.write(f"Cell count: {len(umi_ratios)}\n")
        output_buffer.write(f"Ratio statistics\n")
        output_buffer.write(f"Mean: {mean_r}\nMedian: {median_r}\nMode: {mode_r}\nVariance: {variance_r}\n")
        output_buffer.write(f"UMI count statistics\n")
        output_buffer.write(f"Mean: {mean_c}\nMedian: {median_c}\nMode: {mode_c}\nVariance: {variance_c}\n")
        output = output_buffer.getvalue()

    if output_file is None:
        print(output)
    else:
        with open(output_file, "w") as out:
            out.write(output)


