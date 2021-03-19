These are some tools for working with gRNA/mRNA data in the format of MatrixMarket files.

For Guide RNA, the format of the files is

### Header:
"Unique Guide RNA ID Count" "Unique Cell ID Count" "UMI Count"

### Body:
"Guide RNA ID" "Cell ID" "UMI"

ex:
```
% lines that begin with a percent are comments
% they can only be at the beginning of the file
%
827394 982394 98273987234
123 1 1
334 1 4
432 1 1
123 2 5
908 2 1
432 2 1
```

For mRNA, the format of the files is similar.

### Header:
"Unique mRNA ID Count" "Unique Cell ID Count" "UMI Count"

### Body:
"mRNA ID" "Cell ID" "UMI"

Each tool has some built-in help if you run it with the `-h` flag.

## gen_cell_counts.py
The input is a matrix market file. The output is a file with two columns,
"Cell ID Count" and "Cell ID". Each row represents a particular cell ID in the input file.

## gen_stats.py
Generates some basic statistics about cell counts. The input would be the output of `gen_cell_counts.py`.
The output looks like

```
Mean: 1719.8179213107837
Median: 1793.0
Mode: 34
Variance: 1129369.5144461421
```

## gen_hist.py
Creates a histogram using matplotlib. The input would be the output of `gen_cell_counts.py` or any list of numbers, one per line. The output is an image of a histogram of the data.

## gen_guide_combos.py
This tool generates all the gRNA combinations of size k chosen from the set of gRNAs shared by each pair of cells. The input is a matrix market file. The output is a file with 4 fields: "k", "cell ID 1", "cell ID 2", "gRNA combination"

ex. `2 34 657 (123, 456)`

## gen_cells_per_guide_combo.py
`gen_cells_per_guide_combo.py` "pivots" the output of `gen_guide_combos.py`. The result is a file that gives all the cells that share a particular combination of gRNAs. This results in each line being a variable length record of the format: "gRNA combination", "number of cells with combination", "cell 1", "cell 2"[, "cell 3"...]

ex. `(123,456) 4 123 6 95609586 6778`

## gen_combo_plot.py
`gen_combo_plot.py` is an experiment to generate a useful visualization of the output of `gen_cells_per_guide_combo.py`. Not yet successful.
