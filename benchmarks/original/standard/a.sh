for i in *.bench
do
	a=$(basename "$i" .bench)
	mkdir $a
	x=1
	while [ $x -le 50 ]
	do
		python sar.py $i
		x=$(( $x + 1 ))
	done

	for k in *_enc-*.bench
	do
		mv $k $a
	done
done
