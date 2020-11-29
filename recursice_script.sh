#!/bin/bash
for i in {1..20000}
do
./a.out > tmp_2.txt
dmesg >tmp.txt  
cat tmp.txt | tail -n 1
done

