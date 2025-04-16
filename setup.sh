#!/bin/bash
if [ -d "data" ]; then
    rm -r -f "data"
    echo -e "Removed old data materials.\n"
fi

echo -e "Generating data directory...\n"
mkdir data

echo -e "Downloading metadata..."
cd data
curl -O https://os.unil.cloud.switch.ch/fma/fma_metadata.zip
OUTPUT=`echo "f0df49ffe5f2a6008d7dc83c6915b31835dfe733  fma_metadata.zip" | sha1sum -c -`

if [ "$OUTPUT" == "fma_metadata.zip: OK" ]; then
    echo -e "fma_metadata.zip downloaded properly. Unpacking.\n"
else
    echo -e "fma_metadata.zip downloaded improperly. Please retry.\n"
    exit
fi

unzip fma_metadata.zip

rm fma_metadata.zip

cd ..

echo -e "Finished setup. Exitting.\n\n"