#!/bin/bash

DIR=bron-kerbosch

OUTPUT_NX_DIR=$DIR/nx
OUTPUT_STD_DIR=$DIR/std

DATE=`date -I'seconds' | sed 's/+.*//'`

COMPARISON_LOG=$DIR/$DATE.log

GRAPHS_DIR=konect.cc

GRAPHS_PATH=`find . -type f -name "*edges" -exec echo {} \;`
# echo $GRAPHS_PATH

SEC=120

uname -a > $COMPARISON_LOG
uname -a
date >> $COMPARISON_LOG
date

if [ ! -d "$OUTPUT_NX_DIR" ]; then
    mkdir "$OUTPUT_NX_DIR"
fi

if [ ! -d "$OUTPUT_STD_DIR" ]; then
    mkdir "$OUTPUT_STD_DIR"
fi

echo "-------------------------"
for filepath in $GRAPHS_PATH
do
    TIMEOUT=1

    filename=$(basename ${filepath} | sed 's/.edges$//')
    # echo $FILE
    timeout $SEC $DIR/find-cliques.py --file ${filepath} --output $OUTPUT_NX_DIR/${filename}_unsorted --mode "standard" -c $COMPARISON_LOG -k 4

    if [ $? -eq 124 ]; then
        echo "!!! ${SEC} seconds timeout expired"
        TIMEOUT=0
    else
        cat $OUTPUT_NX_DIR/${filename}_unsorted | sort > $OUTPUT_NX_DIR/${filename}.out
	    rm -f $OUTPUT_NX_DIR/${filename}_unsorted
    fi


    timeout $SEC $DIR/find-cliques.py --file ${filepath} --output $OUTPUT_STD_DIR/${filename}_unsorted --mode "nx" -c $COMPARISON_LOG -k 4

    if [ $? -eq 124 ]; then
        echo "!!! ${SEC} seconds timeout expired"
        TIMEOUT=0
    else
        cat $OUTPUT_STD_DIR/${filename}_unsorted | sort > $OUTPUT_STD_DIR/${filename}.out
	    rm -f $OUTPUT_STD_DIR/${filename}_unsorted
    fi



    if [ $TIMEOUT -eq 1 ]; then
        echo comparing $OUTPUT_NX_DIR/${filename}.out $OUTPUT_STD_DIR/${filename}.out >> $COMPARISON_LOG
        diff $OUTPUT_NX_DIR/${filename}.out $OUTPUT_STD_DIR/${filename}.out >> $COMPARISON_LOG
    fi

	echo "-------------------------"
done


# comment to disable
#COMPUTE_KONECT=yes
#if [ ! -z "$COMPUTE_KONECT" ]   # enter this section
#then

#fi



