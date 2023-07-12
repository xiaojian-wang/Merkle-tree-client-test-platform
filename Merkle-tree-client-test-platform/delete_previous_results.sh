#!/bin/bash

# Delete existing files if they exist
for i in {1..10}
do
    sample_rate=$(bc <<< "scale=1; $i/10")
    filename=$(printf "verify_time_%.1f.txt" $sample_rate)
    if [[ -f $filename ]]; then
        rm $filename
    fi
done