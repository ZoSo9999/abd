#!/bin/bash

BERLOWITZ_DIR=../berlowitz
TWO_PLEXES_DIR=../two-plexes-cikm
OUTPUT_BERLOWITZ_DIR=output_berlowitz
OUTPUT_CIKM_DIR=output_cikm

COMPARISON_LOG=comparison.log

GRAPHS_DIR=../network-repository/konect.cc/10-100-nodes/brunson_club_membership
# GRAPHS_DIR=../networks/toy_examples
# GRAPHS_DIR=../networks/daDonatella

GRAPHS=`ls $GRAPHS_DIR | grep edges`
# echo $GRAPHS

# TIMEOUT = number of seconds 3600=1 hour; 43200=12 hours; 86400=24 hours
#
TIMEOUT=86400

# INTERVAL = interval between checks if the process is still alive. 
#            Positive integer, default value: 1 seconds.
INTERVAL=30
        
# DELAY = delay between posting the SIGTERM signal and destroying the
#         process by SIGKILL. Default value: 1 seconds.
DELAY=1

# Comment the next line if you don't want any timeout 
#
TIMEOUT_COMMAND="./timeout3.sh -t $TIMEOUT -i $INTERVAL -d $DELAY" 
#echo TIMEOUT_COMMAND = $TIMEOUT_COMMAND

uname -a > $COMPARISON_LOG
uname -a
date >> $COMPARISON_LOG
date
echo "timeout = $TIMEOUT"
echo "timeout = $TIMEOUT" >> $COMPARISON_LOG


echo "-------------------------"
for filename in $GRAPHS
do
	echo $filename `../network-repository/get_node_edge_number.sh $GRAPHS_DIR/$filename`

	$TIMEOUT_COMMAND $TWO_PLEXES_DIR/two_plexes_cikm.py --file=$GRAPHS_DIR/$filename --minsize=2 --output=$OUTPUT_CIKM_DIR/${filename}_unsorted --type=all 
	ERROR_CODE=$?
	if [ ${ERROR_CODE} -eq 143 ] # 143 = I was killed by SIGINT
    then
        echo "   CIKM-B: seconds for enumerating ??? connected 2-plexes: $TIMEOUT"
    fi 
	cat $OUTPUT_CIKM_DIR/${filename}_unsorted | sort > $OUTPUT_CIKM_DIR/${filename}.out
	rm -f $OUTPUT_CIKM_DIR/${filename}_unsorted

	$TIMEOUT_COMMAND python2 $BERLOWITZ_DIR/kplex.py --file="$GRAPHS_DIR/$filename" --k=2 --type="unconnected" --output="$OUTPUT_BERLOWITZ_DIR/$filename" --num_of_kplex=999999999
	ERROR_CODE=$?
	if [ ${ERROR_CODE} -eq 143 ] # 143 = I was killed by SIGINT
    then
        echo "BERLOWITZ: seconds for enumerating ??? connected 2-plexes: $TIMEOUT"
    fi 
	cat $OUTPUT_BERLOWITZ_DIR/${filename}_unconnected | sort > $OUTPUT_BERLOWITZ_DIR/${filename}.out
	rm -f $OUTPUT_BERLOWITZ_DIR/${filename}_unconnected

    echo comparing $OUTPUT_CIKM_DIR/${filename}.out $OUTPUT_BERLOWITZ_DIR/${filename}.out >> $COMPARISON_LOG
	diff $OUTPUT_CIKM_DIR/${filename}.out $OUTPUT_BERLOWITZ_DIR/${filename}.out >> $COMPARISON_LOG

	echo "-------------------------"
done


# comment to disable
#COMPUTE_KONECT=yes
#if [ ! -z "$COMPUTE_KONECT" ]   # enter this section
#then

#fi



