#!/bin/bash
for i in *.bench
do
	exec 3< cmd.txt
	a='~/abc/abc -c "read_bench '"$i"'"'
	while read 0<&3 line;
	do
		b="$(echo ${line})"
	done
	exec 3<&-
	c="$( echo "$i" | head -n1 | cut -d "_" -f1 )"
	echo ''"$a $b"' -c "write_bench -l '"$c"'_opt.bench"'
done

