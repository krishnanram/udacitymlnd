#!/bin/bash

echo $1 $2 $3 $4 $5 $6;
rmtrash logs/$1/findOptimal*.log
rmtrash logs/$1/runTimeStat.json
while sleep 1;
do 
 python findOptimalParams.py $1 $2 $3 $4 $5 $6;
 if [ $? -ne 0 ]; then
	echo "Rerunning findOptimalParams.py"
 else
    echo "All Done"
	exit
 fi
 sleep 3
done
