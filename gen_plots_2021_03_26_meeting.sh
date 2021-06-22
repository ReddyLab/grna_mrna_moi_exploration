# lexi/guide.mtx copied from HARDAC:
# /gpfs/fs1/data/gersbachlab/susan/susan/10x/lexi/guide.mtx.gz

echo "generate all the guide combinations of size k (default 2) in each cell"
./gen_guide_combos.py -i lexi/guide.mtx -o lexi/guide_combinations_2.txt
# k = 3, 4, and especially 5 generate large files and shouldn't be run by default.
# ./gen_guide_combos.py -i lexi/guide.mtx -o lexi/guide_combinations_3.txt -k 3
# ./gen_guide_combos.py -i lexi/guide.mtx -o lexi/guide_combinations_4.txt -k 4
# ./gen_guide_combos.py -i lexi/guide.mtx -o lexi/guide_combinations_5.txt -k 5

echo "generate a list of cells with each guide combinations"
./gen_cells_per_guide_combo.py -i lexi/guide_combinations_2.txt -o lexi/guide_cells_per_combo_2.txt

# 3, 4, and especially 5 generate very large files and require a huge amount of memory
# and shouldn't be run by default.
# ./gen_cells_per_guide_combo.py -i lexi/guide_combinations_3.txt -o lexi/guide_cells_per_combo_3.txt
# ./gen_cells_per_guide_combo.py -i lexi/guide_combinations_4.txt -o lexi/guide_cells_per_combo_4.txt
# ./gen_cells_per_guide_combo.py -i lexi/guide_combinations_5.txt -o lexi/guide_cells_per_combo_5.txt

echo "add guide ids to lexi_scrna.guides.txt"
awk '{print NR, $0}' lexi/lexi_scrna.guides.txt > lexi/lexi_scrna_guideid_guide.txt

echo "filter out guide combinations that are reverse compliments (within the bounds of a minimum edit distance) of each other"
./gen_cells_per_guide_combo_rc_filter.py -i lexi/guide_cells_per_combo_2.txt \
  -g lexi/lexi_scrna_guideid_guide.txt \
  -t 1 \
  -o lexi/guide_cells_per_combo_2_filtered_1.txt

./gen_cells_per_guide_combo_rc_filter.py -i lexi/guide_cells_per_combo_2.txt \
  -g lexi/lexi_scrna_guideid_guide.txt \
  -t 2 \
  -o lexi/guide_cells_per_combo_2_filtered_2.txt

./gen_cells_per_guide_combo_rc_filter.py -i lexi/guide_cells_per_combo_2.txt \
  -g lexi/lexi_scrna_guideid_guide.txt \
  -t 1 \
  -r \
  -o lexi/guide_cells_per_combo_2_filtered_1r.txt

./gen_cells_per_guide_combo_rc_filter.py -i lexi/guide_cells_per_combo_2.txt \
  -g lexi/lexi_scrna_guideid_guide.txt \
  -t 2 \
  -r \
  -o lexi/guide_cells_per_combo_2_filtered_2r.txt

echo "Chromosome location vs. \"co-occurrance\" measure"
# Co-occurrance measure of a pair of guides is x/p where
#  x = how many cells those guides are in together
#  p = how many total guides pairs there are

# Plot based on various filterings
P=`wc -l lexi/guide_cells_per_combo_2.txt | awk '{print $1}'`
./gen_cooccurrance_plot.py -i lexi/guide_cells_per_combo_2.txt -g lexi/lexi_scrna_guideid_guide.txt \
  -p ${P} \
  -o lexi/guide_cooccurrance_chrom_dist_plot.png \
  -t "co-occurrance by chromosomal distance"

./gen_cooccurrance_plot.py -i lexi/guide_cells_per_combo_2.txt -g lexi/lexi_scrna_guideid_guide.txt \
  -p ${P} \
  -o lexi/guide_cooccurrance_chrom_dist_plot_edit_dist.png \
  --edit-dist \
  -y "edit distance" \
  -t "co-occurrance by edit distance"

./gen_cooccurrance_plot.py -i lexi/guide_cells_per_combo_2.txt -g lexi/lexi_scrna_guideid_guide.txt \
  -p ${P} \
  -o lexi/guide_cooccurrance_chrom_dist_plot_rev_edit_dist.png \
  --rev-edit-dist \
  -y "edit distance of rev. comp." \
  -t "co-occurrance by reverse compliment edit distance"

./gen_cooccurrance_plot.py -i lexi/guide_cells_per_combo_2.txt -g lexi/lexi_scrna_guideid_guide.txt \
  -p ${P} \
  -o lexi/guide_cooccurrance_chrom_dist_plot_min_edit_dist.png \
  --min-edit-dist \
  -y "min(edit distance, edit distance of rev. comp.)" \
  -t "co-occurrance by min(edit distance, rev. comp. edit distance)"

P=`wc -l lexi/guide_cells_per_combo_2_filtered_1.txt | awk '{print $1}'`
./gen_cooccurrance_plot.py -i lexi/guide_cells_per_combo_2_filtered_1.txt -g lexi/lexi_scrna_guideid_guide.txt \
  -p ${P} \
  -t "co-occurrance by chromosomal distance\n(guides filtered by edit distance > 1)" \
  -o lexi/guide_cooccurrance_chrom_dist_plot_filter_1.png

./gen_cooccurrance_plot.py -i lexi/guide_cells_per_combo_2_filtered_1.txt -g lexi/lexi_scrna_guideid_guide.txt \
  -p ${P} \
  -o lexi/guide_cooccurrance_chrom_dist_plot_edit_dist_filter_1.png \
  --edit-dist \
  -y "edit distance" \
  -t "co-occurrance by edit distance\n(guides filtered by edit distance > 1)"

./gen_cooccurrance_plot.py -i lexi/guide_cells_per_combo_2_filtered_1.txt -g lexi/lexi_scrna_guideid_guide.txt \
  -p ${P} \
  -o lexi/guide_cooccurrance_chrom_dist_plot_rev_edit_dist_filter_1.png \
  --rev-edit-dist \
  -y "edit distance of rev. comp." \
  -t "co-occurrance by reverse compliment edit distance\n(guides filtered by edit distance > 1)"

./gen_cooccurrance_plot.py -i lexi/guide_cells_per_combo_2_filtered_1.txt -g lexi/lexi_scrna_guideid_guide.txt \
  -p ${P} \
  -o lexi/guide_cooccurrance_chrom_dist_plot_min_edit_dist_filter_1.png \
  --min-edit-dist \
  -y "min(edit distance, edit distance of rev. comp.)" \
  -t "co-occurrance by co-occurrance by min(edit distance, rev. comp. edit distance)\n(guides filtered by edit distance > 1)"

P=`wc -l lexi/guide_cells_per_combo_2_filtered_2.txt | awk '{print $1}'`
./gen_cooccurrance_plot.py -i lexi/guide_cells_per_combo_2_filtered_2.txt -g lexi/lexi_scrna_guideid_guide.txt \
  -p ${P} \
  -t "co-occurrance by chromosomal distance\n(guides filtered by edit distance > 2)" \
  -o lexi/guide_cooccurrance_chrom_dist_plot_filter_2.png

./gen_cooccurrance_plot.py -i lexi/guide_cells_per_combo_2_filtered_2.txt -g lexi/lexi_scrna_guideid_guide.txt \
  -p ${P} \
  -o lexi/guide_cooccurrance_chrom_dist_plot_edit_dist_filter_2.png \
  --edit-dist \
  -y "edit distance" \
  -t "co-occurrance by edit distance\n(guides filtered by edit distance > 2)"

./gen_cooccurrance_plot.py -i lexi/guide_cells_per_combo_2_filtered_2.txt -g lexi/lexi_scrna_guideid_guide.txt \
  -p ${P} \
  -o lexi/guide_cooccurrance_chrom_dist_plot_rev_edit_dist_filter_2.png \
  --rev-edit-dist \
  -y "edit distance of rev. comp." \
  -t "co-occurrance by reverse compliment edit distance\n(guides filtered by edit distance > 2)"

./gen_cooccurrance_plot.py -i lexi/guide_cells_per_combo_2_filtered_2.txt -g lexi/lexi_scrna_guideid_guide.txt \
  -p ${P} \
  -o lexi/guide_cooccurrance_chrom_dist_plot_min_edit_dist_filter_2.png \
  --min-edit-dist \
  -y "min(edit distance, edit distance of rev. comp.)" \
  -t "co-occurrance by co-occurrance by min(edit distance, rev. comp. edit distance)\n(guides filtered by edit distance > 2)"

P=`wc -l lexi/guide_cells_per_combo_2_filtered_1r.txt | awk '{print $1}'`
./gen_cooccurrance_plot.py -i lexi/guide_cells_per_combo_2_filtered_1r.txt -g lexi/lexi_scrna_guideid_guide.txt \
  -p ${P} \
  -t "co-occurrance by chromosomal distance\n(guides filtered by edit distance > 1 inc. rev. compliment)" \
  -o lexi/guide_cooccurrance_chrom_dist_plot_filter_1r.png

./gen_cooccurrance_plot.py -i lexi/guide_cells_per_combo_2_filtered_1r.txt -g lexi/lexi_scrna_guideid_guide.txt \
  -p ${P} \
  -o lexi/guide_cooccurrance_chrom_dist_plot_edit_dist_filter_1r.png \
  --edit-dist \
  -y "edit distance" \
  -t "co-occurrance by edit distance\n(guides filtered by edit distance > 1 inc. rev. compliment)"

./gen_cooccurrance_plot.py -i lexi/guide_cells_per_combo_2_filtered_1r.txt -g lexi/lexi_scrna_guideid_guide.txt \
  -p ${P} \
  -o lexi/guide_cooccurrance_chrom_dist_plot_rev_edit_dist_filter_1r.png \
  --rev-edit-dist \
  -y "edit distance of rev. comp." \
  -t "co-occurrance by reverse compliment edit distance\n(guides filtered by edit distance > 1 inc. rev. compliment)"

./gen_cooccurrance_plot.py -i lexi/guide_cells_per_combo_2_filtered_1r.txt -g lexi/lexi_scrna_guideid_guide.txt \
  -p ${P} \
  -o lexi/guide_cooccurrance_chrom_dist_plot_min_edit_dist_filter_1r.png \
  --min-edit-dist \
  -y "min(edit distance, edit distance of rev. comp.)" \
  -t "co-occurrance by co-occurrance by min(edit distance, rev. comp. edit distance)\n(guides filtered by edit distance > 1 inc. rev. compliment)"

P=`wc -l lexi/guide_cells_per_combo_2_filtered_2r.txt | awk '{print $1}'`
./gen_cooccurrance_plot.py -i lexi/guide_cells_per_combo_2_filtered_2r.txt -g lexi/lexi_scrna_guideid_guide.txt \
  -p ${P} \
  -t "co-occurrance by chromosomal distance\n(guides filtered by edit distance > 2 inc. rev. compliment)" \
  -o lexi/guide_cooccurrance_chrom_dist_plot_filter_2r.png

./gen_cooccurrance_plot.py -i lexi/guide_cells_per_combo_2_filtered_2r.txt -g lexi/lexi_scrna_guideid_guide.txt \
  -p ${P} \
  -o lexi/guide_cooccurrance_chrom_dist_plot_edit_dist_filter_2r.png \
  --edit-dist \
  -y "edit distance" \
  -t "co-occurrance by edit distance\n(guides filtered by edit distance > 2 inc. rev. compliment)"

./gen_cooccurrance_plot.py -i lexi/guide_cells_per_combo_2_filtered_2r.txt -g lexi/lexi_scrna_guideid_guide.txt \
  -p ${P} \
  -o lexi/guide_cooccurrance_chrom_dist_plot_rev_edit_dist_filter_2r.png \
  --rev-edit-dist \
  -y "edit distance of rev. comp." \
  -t "co-occurrance by reverse compliment edit distance\n(guides filtered by edit distance > 2 inc. rev. compliment)"

./gen_cooccurrance_plot.py -i lexi/guide_cells_per_combo_2_filtered_2r.txt -g lexi/lexi_scrna_guideid_guide.txt \
  -p ${P} \
  -o lexi/guide_cooccurrance_chrom_dist_plot_min_edit_dist_filter_2r.png \
  --min-edit-dist \
  -y "min(edit distance, edit distance of rev. comp.)" \
  -t "co-occurrance by co-occurrance by min(edit distance, rev. comp. edit distance)\n(guides filtered by edit distance > 2 inc. rev. compliment)"

echo "how many guides each cell has"
tail -n +5 lexi/guide.mtx | awk '{if($3 > 4) {print $2}}' | uniq -c | sort -k 1n,2n > lexi/guides_per_cell.txt
./gen_hist.py -i lexi/guides_per_cell.txt \
    -o lexi/guides_per_cell_hist.png \
    -b 140 \
    -x "Guides per cell" \
    -y "Frequency"

./gen_stats.py -i lexi/guides_per_cell.txt -o lexi/guides_per_cell_stats.txt
wc -l lexi/guides_per_cell.txt
awk '{if($1 == 3){print $1, $2}}' lexi/guides_per_cell.txt | wc -l


# Get the ids of the cells from guide pair in the most cells
# plus histogram and stats

CELLS=`sort -k 2n lexi/guide_cells_per_combo_2_filtered.txt | tail -n -1 | awk '{$1 = ""; $2 = ""; print $0}'`
for c in $CELLS; do
  grep -e " $c$" lexi/guides_per_cell.txt >> lexi/guides_per_cell_from_largest_guide_pair_set.txt
done
./gen_hist.py -i lexi/guides_per_cell_from_largest_guide_pair_set.txt \
    -o lexi/guides_per_cell_from_largest_guide_pair_set_hist.png \
    -b 70 \
    -x "Guides per cell" \
    -y "Frequency"

./gen_stats.py -i lexi/guides_per_cell_from_largest_guide_pair_set.txt -o lexi/guides_per_cell_from_largest_guide_pair_set_stats.txt
rm lexi/guides_per_cell_from_largest_guide_pair_set.txt

echo "generate clusters"
rm lexi/guide_cells_per_combo_2_clustered.txt
./gen_clusters.py -i lexi/guide_cells_per_combo_2_filtered.txt -o lexi/guide_cells_per_combo_2_clustered.txt

echo "total cluster count"
grep "##" lexi/guide_cells_per_combo_2_clustered.txt | awk '{if($3 > 0){print $3}}' | wc -l

echo "cluster > 1 count"
grep "##" lexi/guide_cells_per_combo_2_clustered.txt | awk '{if($3 > 1){print $3}}' | wc -l

echo "10 biggest clusters"
grep "##" lexi/guide_cells_per_combo_2_clustered.txt | awk '{print $3}' | sort -rn | head

echo "10 smallest clusters"
grep "##" lexi/guide_cells_per_combo_2_clustered.txt | awk '{print $3}' | sort -n | head

echo "cluster size stats"
grep "##" lexi/guide_cells_per_combo_2_clustered.txt | awk '{print $3}' | ./gen_stats.py -o lexi/guide_cells_per_combo_2_clustered_stats.txt

echo "cluster size histogram"
grep "##" lexi/guide_cells_per_combo_2_clustered.txt | awk '{print $3}' | \
./gen_hist.py -o lexi/guide_cells_per_combo_2_clustered_hist.png \
    -b 700 \
    -x "Cluster size" \
    -y "Frequency"

echo "guide 2-tuple cell count"
awk '{print $2}' lexi/edit_distance_rev_con/guide_cells_per_combo_2_filtered.txt > lexi/counts.txt
./gen_hist.py -i lexi/counts.txt \
    -o lexi/guide_cells_per_combo_2_cell_count_hist.png \
    -b 35 \
    -x "Cells per guide pair" \
    -y "Frequency"

./gen_stats.py -i lexi/counts.txt -o lexi/guide_cells_per_combo_2_stats.txt

echo "guide 3-tuple cell count"
awk '{print $2}' lexi/guide_cells_per_combo_3.txt > lexi/counts.txt
./gen_hist.py -i lexi/counts.txt \
    -o lexi/guide_cells_per_combo_3_cell_count_hist.png \
    -b 110 \
    -x "Cells per guide 3-tuple" \
    -y "Frequency"

./gen_stats.py -i lexi/counts.txt -o lexi/guide_cells_per_combo_3_stats.txt

echo "guide 4-tuple cell count"
awk '{print $2}' lexi/guide_cells_per_combo_4.txt > lexi/counts.txt
./gen_hist.py -i lexi/counts.txt \
    -o lexi/guide_cells_per_combo_4_cell_count_hist.png \
    -b 35 \
    -x "Cells per guide 4-tuple" \
    -y "Frequency"

./gen_stats.py -i lexi/counts.txt -o lexi/guide_cells_per_combo_4_stats.txt

rm lexi/counts.txt

echo "how many reads per guide in cells with 1 or 2 guides"
./gen_guide_read_per_cell.py -i lexi/guide.mtx -o lexi/guide_umis_per_cell.txt
awk '{if($2 == 1){print $0}}' lexi/guide_umis_per_cell.txt > lexi/guide_umis_per_cell_1_guide.txt
awk '{if($2 == 2){print $0}}' lexi/guide_umis_per_cell.txt > lexi/guide_umis_per_cell_2_guide.txt

echo "1 guide"
awk '{print $3}' lexi/guide_umis_per_cell_1_guide.txt | awk -F ',' '{print $2}' | tr -d ')' | \
./gen_stats.py -o lexi/guide_umis_per_cell_1_guide_stats.py
awk '{print $3}' lexi/guide_umis_per_cell_1_guide.txt | awk -F ',' '{print $2}' | tr -d ')' | \
./gen_hist.py -o lexi/guide_umis_per_cell_1_guide_hist.png \
  -b 60 \
  -x "UMI Count" \
  -y "Frequency" \
  -t "UMI Counts from Cells with One Guide"

echo "2 guides"
./gen_cell_guide_pair_umi_diffs.py -i lexi/guide_umis_per_cell_2_guide.txt

echo "how many cells are guides in?"
awk '{if($3 > 4){print $1}}' lexi/guide.mtx | sort -n | uniq -c | ./gen_stats.py -o lexi/cells_per_guide_stats.txt
awk '{if($3 > 4){print $1}}' lexi/guide.mtx | sort -n | uniq -c | ./gen_hist.py -o lexi/cells_per_guide_hist.png \
  -b 60 \
  -x "Cell Count" \
  -y "Frequency" \
  -t "UMI Counts from Cells with One Guide"

echo "how many guides in cells in largest single guide pair group"
rm lexi/guide_umis_per_cell_from_largest_guide_pair_set.txt
for c in $CELLS; do
  grep -e "^$c " lexi/guide_umis_per_cell.txt >> lexi/guide_umis_per_cell_from_largest_guide_pair_set.txt
done

awk '{print $2}' lexi/guide_umis_per_cell_from_largest_guide_pair_set.txt | ./gen_stats.py -o lexi/guides_per_cell_from_largest_guide_pair_set_stats.txt
awk '{print $2}' lexi/guide_umis_per_cell_from_largest_guide_pair_set.txt | ./gen_hist.py -o lexi/guides_per_cell_from_largest_guide_pair_set_hist.png \
    -b 40 \
    -x "Guides per cell" \
    -y "Frequency" \
    -t "Guide Cell from Largest Guide Pair set"

echo "What edit distances co-occur with a particular target edit distance?"
./gen_cooccurrance_hist.py -i lexi/guide_umis_per_cell.txt -g lexi/lexi_scrna_guideid_guide.txt -o lexi/gen_cooccurrance_hist -t 0
./gen_hist.py -i lexi/gen_cooccurrance_hist_0 -t "Edit Distances that co-occur with an edit distance of 0" -o lexi/gen_cooccurrance_hist_plot_0.png -x "Edit Distances" -y "Counts"
./gen_hist.py -i lexi/gen_cooccurrance_hist_1 -t "Edit Distances that co-occur with an edit distance of 1" -o lexi/gen_cooccurrance_hist_plot_1.png -x "Edit Distances" -y "Counts"
./gen_hist.py -i lexi/gen_cooccurrance_hist_2 -t "Edit Distances that co-occur with an edit distance of 2" -o lexi/gen_cooccurrance_hist_plot_2.png -x "Edit Distances" -y "Counts"
./gen_hist.py -i lexi/gen_cooccurrance_hist_3 -t "Edit Distances that co-occur with an edit distance of 3" -o lexi/gen_cooccurrance_hist_plot_3.png -x "Edit Distances" -y "Counts"
./gen_hist.py -i lexi/gen_cooccurrance_hist_4 -t "Edit Distances that co-occur with an edit distance of 4" -o lexi/gen_cooccurrance_hist_plot_4.png -x "Edit Distances" -y "Counts"
./gen_hist.py -i lexi/gen_cooccurrance_hist_5 -t "Edit Distances that co-occur with an edit distance of 5" -o lexi/gen_cooccurrance_hist_plot_5.png -x "Edit Distances" -y "Counts"
./gen_hist.py -i lexi/gen_cooccurrance_hist_6 -t "Edit Distances that co-occur with an edit distance of 6" -o lexi/gen_cooccurrance_hist_plot_6.png -x "Edit Distances" -y "Counts"

echo "How many total guides do the cells in the pair with the largest cell count have?"
rm lexi/guide_umis_largest_guide_pair_set.txt
for c in $CELLS; do
    GUIDES=`grep -e"^$c " lexi/guide_umis_per_cell.txt | awk '{$1 = ""; $2 = ""; print $0}'`
    for guide in $GUIDES; do
        echo $guide | awk -F ',' '{print $1}' | tr -d '(' >> lexi/guide_umis_largest_guide_pair_set.txt
    done
done
wc -l lexi/guide_umis_largest_guide_pair_set.txt

echo "How many of those guides are unique?"
sort lexi/guide_umis_largest_guide_pair_set.txt | uniq -c | wc -l

echo "how common are the guides in the pair in the largest number of cells?"
GUIDES=`sort -k 2n lexi/guide_cells_per_combo_2_filtered.txt | tail -n -1 | awk '{print $1}' | tr -d '()' | tr ',' ' '`
for guide in $GUIDES; do
    echo "Guide $guide: \c"
    grep -e "^$guide " lexi/guide.mtx | wc -l
done
rm lexi/guides_per_cell_from_largest_guide_pair_set.txt

echo "What are the actual guides in pairs with the largest number of cells?"
# the following id numbers were generated by
#   sort -rn -k2 lexi/guide_cells_per_combo_2_filtered.txt | awk '{print $1, $2}' | head
# and copied into this document

for id in 2826 3386 2387 2822 2630 2988 2685 3410 2366 3214 2198 3182 2082 3071 1891 7084 2062 2243 1920 3389; do
    grep -e "^$id " lexi/lexi_scrna_guideid_guide.txt
done
