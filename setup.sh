#!/bin/bash
loading_spinner () {
    local spin="-\|/"
    local i=0
    
    while kill -0 $1 2>/dev/null
    do
        i=$(( (i+1) % 4 ))
        printf "\r${spin:$i:1}"
        sleep 0.2
    done
}

echo -e "Downloading metadata..."
curl -O https://os.unil.cloud.switch.ch/fma/fma_metadata.zip
OUTPUT=`echo "f0df49ffe5f2a6008d7dc83c6915b31835dfe733  fma_metadata.zip" | sha1sum -c -`

if [ "$OUTPUT" == "fma_metadata.zip: OK" ]; then
    echo -e "fma_metadata.zip downloaded properly. Installing."
else
    echo -e "fma_metadata.zip downloaded improperly. Please retry.\n"
    exit
fi

unzip -o -q fma_metadata.zip &
loading_spinner $!

rm -f fma_metadata.zip

echo -e "\bFinished install. Parsing file information."

python -I makeCSV.py &
loading_spinner $!

echo -e "\bFinished setup. Exitting."