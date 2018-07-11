x=1
while [ $x -le 3 ]
do
	cd "small-"$x
	for i in *
	do
		echo $i
	done
	cd ../
	x=$(( $x + 1 ))
done