#!/bin/bash

# Makes the bash script to print out every command before it is executed except echo
trap '[[ $BASH_COMMAND != echo* ]] && echo $BASH_COMMAND' DEBUG

n=26
i=0
allFiles=()
while IFS= read -r line; do
	echo $line
	echo $i
	echo $n
	if [ $i -eq $n ] 
	then
		echo i equal to n
		echo "$line"
		allFiles+=($line)
		
		for f in ${allFiles[@]}; do
			echo $f
			rsync -az hpc3:${f} /tmp/$USER/mtvss/data/tmp/video_files
		done
	fi
	i=$((i+1))
done < /tmp/$USER/mtvss/data/tmp/batch_cat1.txt
