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
        '''
        Authors: Jeziel Banos Gonzalez (main), Nathan Mette
        Args: 
            self - self
            file - the csv file which we will be reading the track from

        Purpose: sets up all the term frequencys for different track attributes
                 which will be needed to calculate doc frequency and normalized
                 weights for scoring tracks
            
        '''
        title_tf = {}
        self.title_df = {}
        self.normalized_title_weights ={}

        artist_tf = {}
        self.artist_df = {}
        self.normalized_artist_weights = {}

        album_tf = {}
        self.album_df = {}
        self.normalized_album_weights = {}


        genre_tf = {}

        self.tracks = {} #<-- Nathan Mette's do not touch : {track id: (title, artist name, album name, pop score)}
        
        with open(file, "r", encoding="utf-8") as data_set:
            reader = csv.reader(data_set, quotechar="\"")
            row = 1
            for row in reader:
                title = row[19]
                artist = row[10]
                genres = row[16]
                track_id = row[0]
                album_title = row[5]

                # Add track to dict of all tracks
                self.tracks[track_id] = (title, artist, album_title, row[18])

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
                

                # begin tf for album title
                album_tokens = album_title.lower().split()
                album_tf[track_id] = {}

                for term in album_tokens:
                    if term not in album_tf[track_id]:
                        album_tf[track_id][term] = 1
                    else:
                        album_tf[track_id][term] += 1
                

                # genres
        
        self._calc_df_and_weights("title", title_tf)
        self._calc_df_and_weights("artist",artist_tf)
        self._calc_df_and_weights("album", album_tf)

    def _calc_df_and_weights(self, attribure_string, attribute_tf):
        '''
        Author: Jeziel Banos Gonzalez
        Args:
            self - self
            attribute_string - a string describing what attribute of a track we
                               are attempting to calc the df and norm'd weights for
            attribute_tf -  a dictionary in form {track_id: {term: frequency}} which
                            stores the frequency of each term for each track for a 
                            specified attribute
        
        Purpose: This method calculates the doc frequency and normalized weights for
                 each term for a track's attribute [album title, track title, artist name]
        '''
        df = None
        normalized_weights = None

        # determine the attribute we are calcing for
        match attribure_string:
            case "album":
                df = self.album_df
                normalized_weights = self.normalized_album_weights


            case "artist":
                df = self.artist_df
                normalized_weights = self.normalized_artist_weights

            case "title":
                df = self.title_df
                normalized_weights = self.normalized_title_weights
            
        for track in attribute_tf:

            for term in attribute_tf[track]:
                if term in df:
                    df[term] +=1
                else:
                    df[term] = 1
        
        raw_weights = {}

        # calcing raw weights before normalization
        for track in attribute_tf:
            raw_weights[track] = {}

            for term in attribute_tf[track]:
                raw_weights[track][term] = (1+math.log10(attribute_tf[track][term]))


        # calcing normalized weights
        for track in raw_weights:
            normalized_weights[track] = {}
            square_frequency = [x*x for x in list(raw_weights[track].values())]
            for term in raw_weights[track]:
                cosine = 1/math.sqrt(sum(square_frequency))
                normalized_weights[track][term] = raw_weights[track][term] * cosine
            

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



    def run_query(self, title: str, artist: str, genre: str, album: str):
        return self._run_query(title.lower().split(), artist.lower().split(), genre.lower().split(), album.lower().split())
    
    def _run_query(self, title: list[str], artist: list[str], genre: list[str], album: list[str]):
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

        # Calc albumn tf_idf query weighting
        album_tfidf = {}
        if len(album) != 0:
            album_tfidf = self._calc_ltn(album, self.albumn_df)

        # Add tf_idf weights together
        track_relevance = {}
        title_importance = 3
        artist_importance = 2
        album_importance = 1
        for track_id in self.tracks.keys():
            for term in title_tfidf.keys():
                track_relevance[track_id] = track_relevance.get(track_id, default=0) + title_importance * title_tfidf[term] * self.normalized_title_weights[track_id].get(term, default=0)
            for term in artist_tfidf.keys():
                track_relevance[track_id] = track_relevance.get(track_id, default=0) + artist_importance * artist_tfidf[term] * self.normalized_artist_weights[track_id].get(term, default=0)
            for term in album_tfidf.keys():
                track_relevance[track_id] = track_relevance.get(track_id, default=0) + album_importance * album_tfidf[term] * self.normalized_album_weights[track_id].get(term, default=0)

            # added by Jeziel Banos Gonzalez (just adding popularity score for ties handling)
            track_relevance[track_id] = track_relevance.get(track_id, default=0) + (0.0000005 * self.tracks[track_id][3]) 

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


main("./fma_metadata/trackData.csv")
