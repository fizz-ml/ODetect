wget "http://www.capnobase.org/uploads/media/TBME2013-PPGRR-Benchmark_R3.zip"
mkdir data
mkdir data/raw
mv TBME2013-PPGRR-Benchmark_R3.zip ./data/raw
cd ./data/raw
unzip TBME2013-PPGRR-Benchmark_R3.zip
mv TBME2013-PPGRR-Benchmark_R3 capno
rm TBME2013-PPGRR-Benchmark_R3.zip
cd ../..
