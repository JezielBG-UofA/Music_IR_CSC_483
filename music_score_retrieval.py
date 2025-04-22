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
import math

class IRSystem:

    def __init__(self, file):
        title_tf = {}
        self.title_df = {}
        self.normalized_title_weights ={}
        artist_tf = {}
        self.artist_df = {}
        self.normalized_artist_weights = {}
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
                    if term not in title_tf[track_id]:
                        title_tf[track_id][term] = 1
                    else:
                        title_tf[track_id][term] += 1

                # begin tf for artist
                artist_tokens = artist.lower().split()
                artist_tf[track_id] = {}

                for term in artist_tokens:
                    if term not in artist_tf[track_id]:
                        artist_tf[track_id][term] = 1
                    else:
                        artist_tf[track_id][term] += 1
                

                # begin tf for members

                # genres
        
        self._calc_title_vals(title_tf)
        self._calc_artist_vals(artist_tf)



    def _calc_title_vals(self, title_tf): 
        # calcing doc frequency for titles
        for track in title_tf:
            for term in title_tf[track]:
                if term in self.title_df:
                    self.title_df[term] +=1
                else:
                    self.title_df[term] = 1
        
        title_weights = {} # not normalized

        for track in title_tf:
            title_weights[track] = {}

            for term in title_tf[track]:
                title_weights[track][term] = (1+math.log10(title_tf[track][term]))

        # calcing normalized weights
        for track in title_weights:
            self.normalized_title_weights[track] = {}
            square_frequency = [x*x for x in list(title_weights[track].values())]
            for term in title_weights[track]:
                cosine = 1/math.sqrt(sum(square_frequency))
                self.normalized_title_weights[track][term] = title_weights[track][term] * cosine

    def _calc_artist_vals(self, artist_tf):
        # calcing doc freq for artists
        for track in artist_tf:
            for term in artist_tf[track]:
                if term in self.artist_df:
                    self.artist_df[term] +=1
                else:
                    self.artist_df[term] = 1
        
        artist_weights = {} # not normalized

        for track in artist_tf:
            artist_weights[track] = {}

            for term in artist_tf[track]:
                artist_weights[track][term] = (1+math.log10(artist_tf[track][term]))

        # calcing normalized weights
        for track in artist_weights:
            self.normalized_artist_weights[track] = {}
            square_frequency = [x*x for x in list(artist_weights[track].values())]
            for term in artist_weights[track]:
                cosine = 1/math.sqrt(sum(square_frequency))
                self.normalized_artist_weights[track][term] = artist_weights[track][term] * cosine



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



