'''
Authors: 
    Jeziel Banos Gonzalez
    Nathan Mette
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
        genre_tf = {}

        self.tracks = {}
        
        with open(file, "r") as data_set:
            reader = csv.reader(data_set, quotechar="\"")
            row = 1
            for row in reader:
                title = row[52]
                artist = row[26]
                members = row[25]
                genres = row[42]
                track_id = row[0]

                # Add track to dict of all tracks
                self.tracks[track_id] = title

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


    # Calculates the ltn of the inputted content alongside the df of the provided set.
    def _calc_ltn(self, inputContent: list[str], df: dict[str, int]) -> dict[str, float]:
        # Calc tf of input.
        query_tf = {}
        for term in inputContent:
            query_tf[term] = query_tf.get(term, default=0) + 1

        terms = query_tf.keys()
        
        # Calc l of input.
        query_l = {}
        for term in terms:
            query_l[term] = 1 + math.log10(query_tf[term])

        # Calc t of input.
        query_t = {}
        for term in terms:
            query_t[term] = math.log10(len(self.tracks.keys()) / df[term])

        # Combine and return.
        retVal = {}
        for term in terms:
            retVal[term] = query_l[term] * query_t[term]
        return retVal



    def run_query(self, title: str, artist: str, genre: str):
        return self._run_query(title.lower().split(), artist.lower().split(), genre.lower().split())
    
    def _run_query(self, title: list[str], artist: list[str], genre: list[str]):
        '''
        
        
        '''
        # Calc title_tfidf query weighting
        title_tfidf = {}
        if len(title) != 0:
            title_tfidf = self._calc_ltn(title, self.title_df)
        
        # Calc artist tf_idf query weighting
        artist_tfidf = {}
        if len(artist) != 0:
            artist_tfidf = self._calc_ltn(artist, self.title_df)

        # Can be uncommented once album document calculation complete.
        # Calc albumn tf_idf query weighting
        #album_tfidf = {}
        #if len(album) != 0:
        #    album_tfidf = self._calc_ltn(album, self.albumn_df)

        # Add tf_idf weights together
        track_relevance = {}
        title_importance = 3
        artist_importance = 2
        #album_importance = 1
        for track_id in self.tracks.keys():
            for term in title_tfidf.keys():
                track_relevance[track_id] = track_relevance.get(track_id, default=0) + title_importance * title_tfidf[term] * self.normalized_title_weights[track_id].get(term, default=0)
            for term in artist_tfidf.keys():
                track_relevance[track_id] = track_relevance.get(track_id, default=0) + artist_importance * artist_tfidf[term] * self.normalized_artist_weights[track_id].get(term, default=0)
            #for term in album_tfidf.keys():
            #    track_relevance[track_id] = track_relevance.get(track_id, default=0) + album_importance * album_tfidf[term] * self.normalized_album_weights[track_id].get(term, default=0)

        # Find tracks that can be returned. Any that appear here should be returned before those not in the dictionary.
        possible = {}
        if len(genre) != 0:
            pass # dependent on how genre is stored

        results = []








def main(music_collection):

    ir = IRSystem(music_collection)


    while True:
        queryCheck = input("Please insert a music query. Press enter to continue, if you would like to exit, type \"exit\".")
        if queryCheck.capitalize() == "EXIT":
            break
        title = input("Please provide a title. If no title is desired, simply press ENTER on your keyboard.")
        artist = input("Please provide an artist. If no specific artist is desired, simply press ENTER on your keyboard.")
        genre = input("Please provide a desired genre. Else press ENTER on your keyboard")

        print(ir.run_query(title, artist, genre))



