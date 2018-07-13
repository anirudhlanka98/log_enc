#!/bin/bash
for z in *
do
	if [ -d $z ];then
		cd $z
		for i in *.bench
		do
			exec 3< ../cmd.txt
			a=$(echo '~/Documents/abc/abc -c' '"read_bench '$i'"')
			while read 0<&3 line;
			do
				b=$(echo ${line})
			done
			exec 3<&-
			c=$(echo $i | head -n1 | cut -d "_" -f1 )
			d=$(echo $i | head -n1 | cut -d "-" -f2 )
			g=$(echo $a $b '-c "write_bench -l' $c'_opt-'$d'"')
			eval $g
		done
		mkdir $z"_opt"
		for m in *_opt-*.bench
		do
			mv $m $z"_opt"
		done
		cd ../
	fi
done
	

