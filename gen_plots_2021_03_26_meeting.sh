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


Get the ids of the cells from guide pair in the most cells
plus histogram and stats

CELLS=`sort -k 2n lexi/guide_cells_per_combo_2.txt | tail -n -1 | awk '{$1 = ""; $2 = ""; print $0}'`
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

echo "generate clumps"
rm lexi/guide_cells_per_combo_2_clumped.txt
./gen_clumps.py -i lexi/guide_cells_per_combo_2.txt -o lexi/guide_cells_per_combo_2_clumped.txt

echo "total clump count"
grep "##" lexi/guide_cells_per_combo_2_clumped.txt | awk '{if($3 > 0){print $3}}' | wc -l

echo "clump > 1 count"
grep "##" lexi/guide_cells_per_combo_2_clumped.txt | awk '{if($3 > 1){print $3}}' | wc -l

echo "10 biggest clumps"
grep "##" lexi/guide_cells_per_combo_2_clumped.txt | awk '{print $3}' | sort -rn | head

echo "10 smallest clumps"
grep "##" lexi/guide_cells_per_combo_2_clumped.txt | awk '{print $3}' | sort -n | head

echo "clump size stats"
grep "##" lexi/guide_cells_per_combo_2_clumped.txt | awk '{print $3}' | ./gen_stats.py -o lexi/guide_cells_per_combo_2_clumped_stats.txt

echo "clump size histogram"
grep "##" lexi/guide_cells_per_combo_2_clumped.txt | awk '{print $3}' | \
./gen_hist.py -o lexi/guide_cells_per_combo_2_clumped_hist.png \
    -b 800 \
    -x "Clump size" \
    -y "Frequency"

echo "guide 2-tuple cell count"
awk '{print $2}' lexi/guide_cells_per_combo_2.txt > lexi/counts.txt
./gen_hist.py -i lexi/counts.txt \
    -o lexi/guide_cells_per_combo_2_cell_count_hist.png \
    -b 300 \
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