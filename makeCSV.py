"""
OLD CSV FILES WE NEED TO KEEP -- LOCATION OF WHERE IT IS IN THE CSV
track-id -- 0
album-favorites -- 5
album-listens -- 8
album-producer -- 9
album-tag  -- 10
album-title -- 11
album-tracks -- 12
artist-favorites -- 20
artist-id -- 21
artist-members -- 25
artist-name -- 26
artist-tags -- 28
track-composer -- 35
track-favorites -- 39
track-genre_top -- 40
track-genres (# of genres) -- 41
track-genres-all -- 42
track-interest -- 44
track-listens -- 47
track-title -- 52
"""


"""
HOW TO USE:
    JUST RUN THE PROGRAM, MAKE SURE IT CAN ACCESS THE fma_metadata FOLDER
    IT WILL CREATE A NEW CSV FILE CALLED trackData.csv IN THE fma_metadata FOLDER

    LET ME KNOW IF I NEED TO ADD MORE INFORMATION TO THE CSV FILE
    
    
The CSV file generated will be listed here by:
    0. track-id
    1. album-favorites
    2. album-listens
    3. album-producer
    4. album-tag
    5. album-title
    6. album-tracks
    7. artist-favorites
    8. artist-id
    9. artist-members
    10. artist-name
    11. artist-tags
    12. track-composer
    13. track-favorites
    14. track-genre_top
    15. track-genres (# of genres)
    16. track-genres-all
    17. track-interest
    18. track-listens
    19. track-title
"""

import csv

csvData = [
            0,   # track-id
            5,   # album-favorites
            8,   # album-listens
            9,   # album-producer
            10,  # album-tag
            11,  # album-title
            12,  # album-tracks
            20,  # artist-favorites
            21,  # artist-id
            25,  # artist-members
            26,  # artist-name
            28,  # artist-tags
            35,  # track-composer
            39,  # track-favorites
            40,  # track-genre_top
            41,  # track-genres (# of genres)
            42,  # track-genres-all
            44,  # track-interest
            47,  # track-listens
            52   # track-title
        ]

colNames = [
    "track-id", # 0
    "album-favorites", # 5 
    "album-listens", # 8
    "album-producer", # 9
    "album-tag", # 10
    "album-title", # 11
    "album-tracks", # 12
    "artist-favorites", # 20
    "artist-id", # 21
    "artist-members", # 25 
    "artist-name", # 26
    "artist-tags", # 28
    "track-composer", # 35
    "track-favorites", # 39
    "track-genre_top", # 40
    "track-genres", # 41
    "track-genres-all", # 42
    "track-interest", # 44
    "track-listens", # 47
    "track-title" # 52
]


def isValidRow(row):
    try:
        if(len(row) > max(csvData)):
            if row[0].isnumeric():
                return True
    except:
        return False

def normalizeCols(row):
    values = []
    for col in row:
        if isinstance(col, str):
            col = col.replace('\n', ' ').replace('\r', ' ')
        values.append(col)
    return values

def makeCSV(input_file, output_file):
    # https://stackoverflow.com/questions/9282967/how-to-open-a-file-using-the-open-with-statement
    with open(input_file, mode='r', encoding='utf-8') as infile:
        with open(output_file, mode='w', encoding='utf-8', newline='') as outfile:
        
            reader = csv.reader(infile)
            writer = csv.writer(outfile, quoting=csv.QUOTE_MINIMAL)
        
            writer.writerow(colNames)
            
            # rows = list(reader) # this is reading into memory
            # for row in rows: # this is reading into memory
            
            for row in reader: # this is not reading into memory DW
                if isValidRow(row):
                    cleaned_row = normalizeCols(row)
                    selected = []
                    for i in csvData:
                        selected.append(cleaned_row[i])
                    writer.writerow(selected)


makeCSV("fma_metadata/tracks.csv", "fma_metadata/trackData.csv")