'''
Authors: 
    Jeziel Banos Gonzalez
    Nathan Mette
    Miro Vanek
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
        self.genre_df = {}
        self.normalized_genre_weights = {}

        self.stopChars = ['-', ' ', ':', '.', '&', '(', ')', '/']



        self.tracks = {} #<-- Nathan Mette's do not touch : {track id: (title, artist name, album name, pop score)}
                            # Miro touched it : {track id: (title, artist name, album name, pop score, genres)}



        genres_translation = {}
        f = open("fma_metadata/genres.csv", "r", encoding="utf-8")
        for line in f:
            line = line.strip().split(",")
            id = line[0].strip()
            title = line[3].strip().lower()
            genres_translation[id]=title
        f.close()



        with open(file, "r", encoding="utf-8") as data_set:
            reader = csv.reader(data_set, quotechar="\"")
            row = 1
            for row in reader:
                #skips the first line of the csv
                if not row[0].isnumeric():
                    continue
                title = row[19]
                artist = row[10]
                genres = row[15]
                track_id = row[0]
                album_title = row[5]

                # Add track to dict of all tracks
                self.tracks[track_id] = (title, artist, album_title, row[18], genres)

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
                

                # begin tf for genres
                raw_genre_ids = genres.strip("\"[").strip("]\"").split(",")
                genre_ids = []
                for i in range(len(raw_genre_ids)):
                    if raw_genre_ids[i].strip() == "":
                        genre_ids.append('NONE')
                    else:
                        translation:str = genres_translation[raw_genre_ids[i].strip()]
                        types = [translation]
                        if '/' in translation:
                            types = translation.split('/')
                        elif '(' in translation:
                            types = translation.replace(')', '').split('(')
                        elif ' - ' in translation:
                            types = translation.split(' - ')
                        
                        for genre in types:
                            genre_ids.append(''.join([x.lower() if x not in self.stopChars else '' for x in genre]))



                genre_tf[track_id] = {}
                for term in genre_ids:
                    if term not in genre_tf[track_id]:
                        genre_tf[track_id][term] = 1
                    else:
                        genre_tf[track_id][term] += 1
        
        self._calc_df_and_weights("title", title_tf)
        self._calc_df_and_weights("artist",artist_tf)
        self._calc_df_and_weights("album", album_tf)
        self._calc_df_and_weights("genre", genre_tf)

    def _calc_df_and_weights(self, attribure_string, attribute_tf):
        '''
        Authors: Jeziel Banos Gonzalez & Miro Vanek
        Args:
            self - self
            attribute_string - a string describing what attribute of a track we
                               are attempting to calc the df and norm'd weights for
            attribute_tf -  a dictionary in form {track_id: {term: frequency}} which
                            stores the frequency of each term for each track for a 
                            specified attribute
        
        Purpose: This method calculates the doc frequency and normalized weights for
                 each term for a track's attribute [album title, track title, artist name, genre]
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
            
            case "genre":
                df = self.genre_df
                normalized_weights = self.normalized_genre_weights
            
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
            

    def _calc_ltn(self, inputContent: list[str], df: dict[str, int]) -> dict[str, float]:
        '''
        Authors: Nathan Mette (main)
        Args:
            self - self
            inputContent - A list of all tokens in the input.
            df - A dictionary containting a [str, int] pairing where the keys are the relevant
                 term and the values are the document frequency related to that term.

        Purpose: Calculates the ltn of the entered list of tokens.
        '''
        # Calc tf of input.
        query_tf = {}
        for term in inputContent:
            query_tf[term] = query_tf.get(term, 0) + 1
        
        retVal = {}
        for term in query_tf.keys():
            if df.get(term, -1) == -1:
                continue
            # Calc l of input.
            query_l = 1 + math.log10(query_tf[term])
            # Calc t of input.
            query_t = math.log10(len(self.tracks.keys()) / df[term])
            # Combine
            retVal[term] = query_l * query_t
        
        return retVal



    def run_query(self, title: str, artist: str, album: str, genre: str, count: int =10) -> list:
        '''
        Authors: Jeziel Banos Gonzalez (main)
        Args: 
            self - self
            title - The user input related to the title query.
            artist - The user input related to the artist query.
            album - The user input related to the album query.
            genre - The user input related to the genre query.
            count - The number of relevant tracks to return.

        Purpose: Normalizes user input and passes it to a helper function to determine query results.
        '''
        genrePass = ''.join([x.lower() if x not in self.stopChars else '' for x in genre])
        return self._run_query(title.lower().split(), artist.lower().split(), album.lower().split(), genrePass, count)
    
    def _run_query(self, title: list[str], artist: list[str], album: list[str], genre: list[str], count) -> list:
        '''
        Authors: Nathan Mette (main), Jeziel Banos Gonzales, Miro Vanek
        Args: 
            self - self
            title - A list of tokens inputted by the user corresponding to the title information.
            artist - A list of tokens inputted by the user corresponding to the artist information.
            album - A list of tokens inputted by the user corresponding to the album information.
            genre - A list of tokens inputted by the user corresponding to the genre information.
            count - The number of relevant tracks to return.

        Purpose: Calculates the tf_idf weighting of every input the user provided and returns a list
                 of all documents related to the query sorted in descending order based on weight.
                 Title, Artist, Album, and Genre are all weighted calculations.
        '''
        # Calc title_tfidf query weighting
        title_tfidf = {}
        if len(title) != 0:
            title_tfidf = self._calc_ltn(title, self.title_df)
        
        # Calc artist tf_idf query weighting
        artist_tfidf = {}
        if len(artist) != 0:
            artist_tfidf = self._calc_ltn(artist, self.artist_df)

        # Calc album tf_idf query weighting
        album_tfidf = {}
        if len(album) != 0:
            album_tfidf = self._calc_ltn(album, self.album_df)

        # Calc genre tf_idf query weighting
        genre_tfidf = {}
        if len(genre) != 0:
            genre_tfidf = self._calc_ltn([genre], self.genre_df)


        # Add tf_idf weights together
        track_relevance : dict[str, float] = {}
        title_importance = 4
        artist_importance = 3
        album_importance = 2
        genre_importance = 1
        for track_id in self.tracks.keys():
            for term in title_tfidf.keys():
                track_relevance[track_id] = track_relevance.get(track_id, 0) + title_importance * title_tfidf[term] * self.normalized_title_weights[track_id].get(term, 0)
            for term in artist_tfidf.keys():
                track_relevance[track_id] = track_relevance.get(track_id, 0) + artist_importance * artist_tfidf[term] * self.normalized_artist_weights[track_id].get(term, 0)
            for term in album_tfidf.keys():
                track_relevance[track_id] = track_relevance.get(track_id, 0) + album_importance * album_tfidf[term] * self.normalized_album_weights[track_id].get(term, 0)
            for term in genre_tfidf.keys():
                track_relevance[track_id] = track_relevance.get(track_id, 0) + genre_importance * genre_tfidf[term] * self.normalized_genre_weights[track_id].get(term, 0)


            # added by Jeziel Banos Gonzalez (just adding popularity score for ties handling)
            track_relevance[track_id] = track_relevance.get(track_id, 0) + (0.0000005 * float(self.tracks[track_id][3])) 

            
        '''
        Nate and Jeziel: This is too inefficient, you are running through all tracks 10 times
        results = []
        #searches for the top 10 track scores
        #Added by Miro Vanek
        for i in range(10):
            cur_max = None
            for id in track_relevance.keys():
                if id not in results:
                    if cur_max == None or track_relevance[id] > track_relevance[cur_max]:
                        cur_max = id
            results.append(cur_max)
        
        #converts each id to the track's title, artist, and album title
        for i in range(len(results)):
            #results[i] = self.tracks[results[i]][:3] Will use, but first test scores
            # Replace with above when finished. Below is just for testing.
            results[i] = (self.tracks[results[i][0]], self.tracks[results[i]][1], self.tracks[results[i]][2], track_relevance[results[i]])
        '''

        sorted_rel = sorted(track_relevance.items(), key=lambda x: x[1], reverse=True)
        # results = [(track title, artist, album, tf_score), ...]
        return [(self.tracks[id][0], self.tracks[id][1], self.tracks[id][2], score) for (id, score) in sorted_rel[:count]]





