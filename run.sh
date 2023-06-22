#!/bin/bash

DIR=bron-kerbosch

OUTPUT_NX_DIR=$DIR/nx
OUTPUT_STD_DIR=$DIR/std

COMPARISON_LOG=$DIR/comparison.log

GRAPHS_DIR=konect.cc

GRAPHS_PATH=`find . -type f -name "*edges" -exec echo {} \;`
# echo $GRAPHS_PATH

uname -a > $COMPARISON_LOG
uname -a
date >> $COMPARISON_LOG
date


echo "-------------------------"
for filename in $GRAPHS_PATH
do
    file=$(basename ${filename} | sed 's/.edges$//')
    # echo $FILE
    $DIR/find-cliques.py -v --file ${filename} --output $OUTPUT_NX_DIR/${file}_unsorted -k 5 --mode nx
	cat $OUTPUT_NX_DIR/${file}_unsorted | sort > $OUTPUT_NX_DIR/${file}.out
	rm -f $OUTPUT_NX_DIR/${file}_unsorted

	# $TIMEOUT_COMMAND python2 $BERLOWITZ_DIR/kplex.py --file="$GRAPHS_DIR/$filename" --k=2 --type="unconnected" --output="$OUTPUT_STD_DIR/$filename" --num_of_kplex=999999999
	# ERROR_CODE=$?
	# if [ ${ERROR_CODE} -eq 143 ] # 143 = I was killed by SIGINT
    # then
    #     echo "BERLOWITZ: seconds for enumerating ??? connected 2-plexes: $TIMEOUT"
    # fi 

	# cat $OUTPUT_STD_DIR/${filename}_unconnected | sort > $OUTPUT_STD_DIR/${filename}.out
	# rm -f $OUTPUT_STD_DIR/${filename}_unconnected

    # echo comparing $OUTPUT_NX_DIR/${filename}.out $OUTPUT_STD_DIR/${filename}.out >> $COMPARISON_LOG
	# diff $OUTPUT_NX_DIR/${filename}.out $OUTPUT_STD_DIR/${filename}.out >> $COMPARISON_LOG

	echo "-------------------------"
done


# comment to disable
#COMPUTE_KONECT=yes
#if [ ! -z "$COMPUTE_KONECT" ]   # enter this section
#then

#fi



