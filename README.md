# Music_IR_CSC_483
## Collaboratively built by: Jeziel Banos Gonzalez, Nathan James Mette, Miro E Vanek, Tony Zhang

### Data Set:
- Original dataset is from the github link found here: https://github.com/mdeff/fma?tab=readme-ov-file 

## Files:
* makeCSV.py
* music_score_retrieval.py
* query.py
* requirements.txt
* setup.sh
* test_queries.py


### How to run:
1. Clone the repo

1. Install dependencies

1. Run the bash script
   ```
   bash setup.sh
   ```
1. Run query.py


### makeCSV.py
- This file is in charge of generating a new csv file called trackData.csv. This generated
  file is utilized by the music IR system to score the different music tracks. This file should
  never be ran by a user, this file will be ran by the setup.sh program

### music_score_retrieval.py
- This is the main file of the project. This file sets up different scores for different tracks, and it holds the IRSystem class.
  the class contains methods for querying for tracks based on user provided input. This file is not meant to be ran, query.py
  is the file that should be ran by users.

### setup.sh
- This file is the first file that should be ran. NOTICE: This file needs to be ran in git bash in order for 
  the program to execute. This program will download the original data set provided for the assignment, which
  is then used by the makeCSV.py program to create the dataset we use for the music score.

### test_queries.py
- This file contains multiple testcases which were used to test if the IR system is working as intended. 
  Not meant to be ran by the user.

### query.py
- This file is meant to be ran by the user to query for music tracks. A user should only run this after setup.sh has been executed.
  A user is able to query by; track name, artist name, genre, album, or any combination of the previous query types. Output will be
  a string listing the top ten tracks that match the query in the following format:
  > this is temp, will update when we finish
