#! /bin/bash
for i in *_keych.bench
do
	a="$( echo "$i" | head -n1 | cut -d "_" -f1 )"
	~/log_dec/bin/sld $i ../../original/upper/$a"_upper.bench"
done