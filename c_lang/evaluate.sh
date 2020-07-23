echo "C language exercises evaluation begins..."
read -p "input number of the exercise:" exnumber

if [ $exnumber -gt 8 ] || [ $exnumber -lt 1 ] ; then
    echo "no lab has been found :(\ntry between 1-8"
    exit
fi

dirr='lab'
dirr+=$exnumber 
read -p "input git path:" gitpath
git clone $gitpath $dirr/gitdir
make -C $dirr 
./$dirr/$dirr
