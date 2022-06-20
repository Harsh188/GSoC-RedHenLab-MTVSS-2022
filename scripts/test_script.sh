#!/bin/bash

echo Hello World!

n=26
i=0
allFiles=()
while IFS= read -r line; do
	if [ $i == $n ] 
	then
		echo "$line"
		allFiles+=($line)
		
		for f in ${allFiles[@]}; do
			echo $f
			rsync -az hpc3:$line /tmp/$USER/${f} /tmp/$USER/mtvss/data/tmp/video_files
		done
	fi
	i=$((i+1))
done < /tmp/$USER/mtvss/data/tmp/batch_cat1.txt
