#!/bin/bash

# Delete existing files if they exist
# for i in {1..10}
# do
#     sample_rate=$(bc <<< "scale=1; $i/10")
#     filename=$(printf "verify_time_%.1f.txt" $sample_rate)
#     if [[ -f $filename ]]; then
#         rm $filename
#     fi
# done

# Run the script 1000 times with increasing sample_rate of 0.1 each time
# for i in {1..10}
# do
#     sample_rate=$(bc <<< "scale=1; $i/10")
#     echo "Running Merkle_test_epoch_len_10.py with sample_rate: $sample_rate"
#     for ((j=1; j<=1000; j++))
#     do
#         python Merkle_test_epoch_len_10.py --sample_rate $sample_rate
#     done
# done
# up code cannot work on android, need to be revised with a version without bc command

#!/bin/bash

# Delete existing files if they exist
for i in {1..10}
do
    sample_rate=$(awk "BEGIN{printf \"%.1f\", $i/10}")
    filename=$(printf "verify_time_%.1f.txt" $sample_rate)
    if [[ -f $filename ]]; then
        rm $filename
    fi
done

# Run the script 1000 times with increasing sample_rate of 0.1 each time
for i in {1..10}
do
    sample_rate=$(awk "BEGIN{printf \"%.1f\", $i/10}")
    echo "Running run_Merkle_test_epoch_len_10_100image.py with sample_rate: $sample_rate"
    for ((j=1; j<=1000; j++))
    do
        python run_Merkle_test_epoch_len_10_100image.py --sample_rate $sample_rate
    done
done
