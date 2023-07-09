#!/bin/bash

# modify theese
SEC=120
K_0=0
K_1=2
K_2=5
K_3=10


DIR=bron-kerbosch
OUTPUT_DIR=$DIR/out
GRAPHS_DIR=konect.cc
GRAPHS_PATH=`find konect.cc -type f -name "*edges" -exec echo {} \;`
CSV=$OUTPUT_DIR/log.csv

if [ ! -d "$OUTPUT_DIR" ]; then
    mkdir "$OUTPUT_DIR"
fi


echo "graph_name; #nodes; #edges; #${K_0}-cliques; tomita-time;; CC-time; #${K_1}-cliques; BK-time;; BK+-time;; CC-time;; CC+-time; #${K_2}-cliques; BK-time;; BK+-time;; CC-time;; CC+-time; #${K_3}-cliques; BK-time;; BK+-time;; CC-time;; CC+-time" >> $CSV

for filepath in $GRAPHS_PATH
do
    filename=$(basename ${filepath} | sed 's/.edges$//')

    timeout $SEC $DIR/find-cliques-bis.py --file ${filepath} --output $CSV --mode standard -k $K_0 --info
    if [ $? -eq 124 ]; then
        python3 $DIR/timeout.py --file ${filepath} --output $CSV --time $SEC --mode all --verbose
    fi

    timeout $SEC $DIR/find-cliques-bis.py --file ${filepath} --output $CSV --mode nx -k $K_0
    if [ $? -eq 124 ]; then
        python3 $DIR/timeout.py --file ${filepath} --output $CSV --time $SEC --mode all --verbose
    fi

    timeout $SEC $DIR/find-cliques-bis.py --file ${filepath} --output $CSV --mode standard -k $K_1
    if [ $? -eq 124 ]; then
        python3 $DIR/timeout.py --file ${filepath} --output $CSV --time $SEC --mode all --verbose
    fi

    timeout $SEC $DIR/find-cliques-bis.py --file ${filepath} --output $CSV --mode nx -k $K_1
    if [ $? -eq 124 ]; then
        python3 $DIR/timeout.py --file ${filepath} --output $CSV --time $SEC --mode all --verbose
    fi

    timeout $SEC $DIR/find-cliques-bis.py --file ${filepath} --output $CSV --mode standard+ -k $K_1
    if [ $? -eq 124 ]; then
        python3 $DIR/timeout.py --file ${filepath} --output $CSV --time $SEC --mode all --verbose
    fi

    timeout $SEC $DIR/find-cliques-bis.py --file ${filepath} --output $CSV --mode nx+ -k $K_1
    if [ $? -eq 124 ]; then
        python3 $DIR/timeout.py --file ${filepath} --output $CSV --time $SEC --mode all --verbose
    fi

    timeout $SEC $DIR/find-cliques-bis.py --file ${filepath} --output $CSV --mode standard -k $K_2
    if [ $? -eq 124 ]; then
        python3 $DIR/timeout.py --file ${filepath} --output $CSV --time $SEC --mode all --verbose
    fi

    timeout $SEC $DIR/find-cliques-bis.py --file ${filepath} --output $CSV --mode nx -k $K_2
    if [ $? -eq 124 ]; then
        python3 $DIR/timeout.py --file ${filepath} --output $CSV --time $SEC --mode all --verbose
    fi

    timeout $SEC $DIR/find-cliques-bis.py --file ${filepath} --output $CSV --mode standard+ -k $K_2
    if [ $? -eq 124 ]; then
        python3 $DIR/timeout.py --file ${filepath} --output $CSV --time $SEC --mode all --verbose
    fi

    timeout $SEC $DIR/find-cliques-bis.py --file ${filepath} --output $CSV --mode nx+ -k $K_2
    if [ $? -eq 124 ]; then
        python3 $DIR/timeout.py --file ${filepath} --output $CSV --time $SEC --mode all --verbose
    fi

    timeout $SEC $DIR/find-cliques-bis.py --file ${filepath} --output $CSV --mode standard -k $K_3
    if [ $? -eq 124 ]; then
        python3 $DIR/timeout.py --file ${filepath} --output $CSV --time $SEC --mode all --verbose
    fi

    timeout $SEC $DIR/find-cliques-bis.py --file ${filepath} --output $CSV --mode nx -k $K_3
    if [ $? -eq 124 ]; then
        python3 $DIR/timeout.py --file ${filepath} --output $CSV --time $SEC --mode all --verbose
    fi

    timeout $SEC $DIR/find-cliques-bis.py --file ${filepath} --output $CSV --mode standard+ -k $K_3
    if [ $? -eq 124 ]; then
        python3 $DIR/timeout.py --file ${filepath} --output $CSV --time $SEC --mode all --verbose
    fi

    timeout $SEC $DIR/find-cliques-bis.py --file ${filepath} --output $CSV --mode nx+ -k $K_3
    if [ $? -eq 124 ]; then
        python3 $DIR/timeout.py --file ${filepath} --output $CSV --time $SEC --mode all --verbose
    fi
    echo >> $CSV
    rm ${filepath}
    echo "ends with ${filename}" 
done




