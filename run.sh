#./shannon_fano_test.py

./sf -c -f $1 
./sf -e -f $1".sf"

echo "compare"
f1=$1
f2=$1".sf.un"

diff $f1 $f2
