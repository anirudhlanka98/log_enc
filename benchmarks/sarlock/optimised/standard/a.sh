for i in *
do
	if [ -d $i ];then
		cd $i
		for x in *
		do
			mv $x ../
		done
		cd ../
	fi
done