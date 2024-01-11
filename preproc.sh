#!/bin/bash
# start in directory with only raw files

# set first N lines to use as header
HEADER_N=11

# create header
for f in `ls *.csv` ; do
    # create header file
    head -n +$HEADER_N ${f} > ../metadata.csv

    # remove header from data file
    START_N="$((HEADER_N-1))"
    tail -n +$START_N ${f} > ../${f}

    # remove units, whitespace
    sed -e '2,3d' ../${f} > ../clean.csv;
    
    mv ../clean.csv ../${f}
done