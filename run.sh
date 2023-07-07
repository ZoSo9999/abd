#!/bin/bash

# modify theese
SEC=5
MODE=standard
K=4


DIR=bron-kerbosch
OUTPUT_DIR=$DIR/out
GRAPHS_DIR=konect.cc
GRAPHS_PATH=`find . -type f -name "*edges" -exec echo {} \;`
CSV=$OUTPUT_DIR/$MODE-$K.csv

if [ ! -d "$OUTPUT_DIR" ]; then
    mkdir "$OUTPUT_DIR"
fi


echo " graph_name; #nodes; #edges; #cliques; time" > $CSV

for filepath in $GRAPHS_PATH
do
    filename=$(basename ${filepath} | sed 's/.edges$//')

    timeout $SEC $DIR/find-cliques.py --file ${filepath} --output $CSV --mode $MODE -k $K

    if [ $? -eq 124 ]; then
        python3 $DIR/timeout.py --file ${filepath} --output $CSV --time $SEC --verbose
    fi
done




