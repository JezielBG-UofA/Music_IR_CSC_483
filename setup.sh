#!/bin/bash

if ! [ -d "data" ]; then
    echo -e "Data directory not found. Generating new data directory...\n"
    mkdir data
fi

echo -e "Downloading metadata..."
cd data
curl -O https://os.unil.cloud.switch.ch/fma/fma_metadata.zip
OUTPUT=`echo "f0df49ffe5f2a6008d7dc83c6915b31835dfe733  fma_metadata.zip" | sha1sum -c -`

if [ "$OUTPUT" == "fma_metadata.zip: OK" ]; then
    echo -e "fma_metadata.zip downloaded properly. Installing."
else
    echo -e "fma_metadata.zip downloaded improperly. Please retry.\n"
    exit
fi

unzip -o -q fma_metadata.zip &
pid=$!

spin="-\|/"

i=0
while kill -0 $pid 2>/dev/null
do
    i=$(( (i+1) %4 ))
    printf "\r${spin:$i:1}"
    sleep 0.5
done

rm -f fma_metadata.zip

cd ..

echo -e "\bFinished setup. Exitting."