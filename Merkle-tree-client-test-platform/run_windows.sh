#!/bin/bash


# Run the script 1000 times with increasing sample_rate of 0.1 each time

for ((j=1; j<=1000; j++))
do
	python Merkle_test_epoch_len_10.py --sample_rate 0.1
done

for ((j=1; j<=1000; j++))
do
	python Merkle_test_epoch_len_10.py --sample_rate 0.2
done

for ((j=1; j<=1000; j++))
do
	python Merkle_test_epoch_len_10.py --sample_rate 0.3
done

for ((j=1; j<=1000; j++))
do
	python Merkle_test_epoch_len_10.py --sample_rate 0.4
done

for ((j=1; j<=1000; j++))
do
	python Merkle_test_epoch_len_10.py --sample_rate 0.5
done

for ((j=1; j<=1000; j++))
do
	python Merkle_test_epoch_len_10.py --sample_rate 0.6
done

for ((j=1; j<=1000; j++))
do
	python Merkle_test_epoch_len_10.py --sample_rate 0.7
done

for ((j=1; j<=1000; j++))
do
	python Merkle_test_epoch_len_10.py --sample_rate 0.8
done

for ((j=1; j<=1000; j++))
do
	python Merkle_test_epoch_len_10.py --sample_rate 0.9
done

for ((j=1; j<=1000; j++))
do
	python Merkle_test_epoch_len_10.py --sample_rate 10
done