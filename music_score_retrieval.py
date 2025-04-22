'''
Authors: 
    Jeziel Banos Gonzalez
    []
    []
    []

File Description:

Instructions:


'''
import csv

class IRSystem:

    def __init__(self, file):
        title_tf = {}
        artist_tf = {}
        members_tf = {}
        genre_tf = {}

        
        with open(file, "r") as data_set:
            reader = csv.reader(data_set, quotechar="\"")
            row = 1
            for row in reader:
                title = row[52]
                artist = row[26]
                members = row[25]
                genres = row[42]
                track_id = row[0]

                # begin tf for title
                title_tokens = title.lower().split()
                title_tf[track_id] = {}

                for term in title_tokens:
                    pass



                # begin tf for artist
                artist_tokens = artist.lower().split()
                artist_tf[track_id] = {}


                # begin tf for members


                # genres





    def run_query(self, title, artist, members, genre):
        return self._run_query(title.lower().split(), artist.lower().split(), members.lower().split(), genre.lower().split())
    
    def _run_query(self, title, artist, members, genre):
        '''
        
        
        '''
        results = []








def main(music_collection):

    ir = IRSystem(music_collection)


    while True:
        queryCheck = input("Please insert a music query. Press enter to continue, if you would like to exit, type \"exit\".")
        if queryCheck.capitalize() == "EXIT":
            break
        title = input("Please provide a title. If no title is desired, simply press ENTER on your keyboard.")
        artist = input("Please provide an artist. If no specific artist is desired, simply press ENTER on your keyboard.")
        members = input("Please provide any members you are interested in, else press ENTER on your keyboard.")
        genre = input("Please provide a desired genre. Else press ENTER on your keyboard")

        print(ir.run_query(title, artist, members, genre))



