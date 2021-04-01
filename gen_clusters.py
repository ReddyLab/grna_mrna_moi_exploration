#!/usr/bin/env python

import argparse
from dataclasses import dataclass, field
import io
import itertools
import math
import sys

@dataclass
class GuidePair:
    guides: tuple[int, int]
    primary_guide: int
    cell_ids: set[str] = field(default_factory=set)

    def __str__(self):
        return f"({self.guides[0]},{self.guides[1]}) {len(self.cell_ids)} {' '.join(sorted(self.cell_ids))})"

@dataclass
class Cluster:
    primary_guide: int
    defining_set: set[int] = field(default_factory=set)
    guide_pairs: list[GuidePair] = field(default_factory=list)

    ## Edit these methods (belongs, add, fit) to change how clustering happens

    def belongs(self, guide_pair):
        return self.fit(guide_pair) > 0

    def add(self, guide_pair):
        self.defining_set |= guide_pair.cell_ids
        self.guide_pairs.append(guide_pair)

    def fit(self, guide_pair):
        return len(self.defining_set | guide_pair.cell_ids)

    def __str__(self):
        cluster_string = None
        with io.StringIO() as cluster_buffer:
            cluster_buffer.write(f"## Cluster! {len(self.guide_pairs)}\n")
            for guide_pair in self.guide_pairs:
                cluster_buffer.write(f"{guide_pair}\n")
            cluster_string = cluster_buffer.getvalue()
        return cluster_string

@dataclass
class Clusters:
    clusters: dict[int, list[Cluster]] = field(default_factory=dict)

    def _add_to_cluster(self, guide_pair):
        if guide_pair.primary_guide not in self.clusters:
            return False

        added = False
        best_clusters = []
        best_cluster_fit = 0
        for cluster in self.clusters[guide_pair.primary_guide]:
            if cluster.belongs(guide_pair):
                fit = cluster.fit(guide_pair)
                if fit > best_cluster_fit:
                    best_clusters = [cluster]
                    best_cluster_fit = fit

                elif fit == best_cluster_fit:
                    best_clusters.append(cluster)
                added = True

        for cluster in best_clusters:
            cluster.add(guide_pair)
        return added

    def empty(self):
        return len(self.clusters) > 0

    def add_guide_pair(self, guide_pair):
        if not self._add_to_cluster(guide_pair):
            cluster_list = self.clusters.get(guide_pair.primary_guide, [])
            cluster = Cluster(primary_guide=guide_pair.primary_guide)
            cluster.add(guide_pair)
            cluster_list.append(cluster)
            self.clusters[guide_pair.primary_guide] = cluster_list

    def __iter__(self):
        for k in self.clusters:
            for cluster in self.clusters[k]:
                yield cluster

    def __str__(self):
        cluster_count = 0
        for k in self.clusters:
            cluster_count += len(self.clusters[k])
        return f"{cluster_count} total clusters"

def get_clusters(grna_sets):
    clusters = Clusters()
    for line in grna_sets:
        pair, count, cell_ids = line.split(maxsplit=2)
        guide_1, guide_2 = pair.strip('()').split(',')
        cell_id_set = set(cell_ids.split())
        clusters.add_guide_pair(GuidePair((int(guide_1), int(guide_2)), int(guide_1), cell_id_set))
        clusters.add_guide_pair(GuidePair((int(guide_1), int(guide_2)), int(guide_2), cell_id_set))
    return clusters

def parse_args():
    parser = argparse.ArgumentParser(description='Processes output of guide_cells_per_guide_combo.py to find "clusters" of cells with the same guide')
    parser.add_argument('-i', '--input', default=None, help="Output from guide_cells_per_guide_combo.py ")
    parser.add_argument('-o', '--output', default=None, help="file with 3 datums: 1) guide pair 2) count of cells with pair 3) list of cells")
    args = parser.parse_args()
    return args.input, args.output

if __name__ == "__main__":
    input_file, output_file = parse_args()

    if input_file is not None:
        with open(input_file) as input:
            clusters = get_clusters(input)
    else:
        clusters = get_clusters(sys.stdin)

    if output_file is None:
        out = sys.stdout
    else:
        out = open(output_file, "w")

    for cluster in clusters:
        out.write(str(cluster))

    if output_file is not None:
        out.close()
