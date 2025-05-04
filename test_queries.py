'''
File: test_queries.py
Author: Jeziel Banos Gonzalez
Purpose: This file is meant to test different queries,  both singe and multi-portion quries
         to verify the IR system developed in file music_score_retrieval.py is returning results
         the make sense. 
'''

import music_score_retrieval

ir = music_score_retrieval.IRSystem("./fma_metadata/trackData.csv")
# ir.run_query(title, artist, album, genre)

def test_genre():
    ir.run_query("","","","Pop")
    

def test_album():
    ir.run_query("","","AWOL - A Way Of Life","")
    

def test_author():
    ir.run_query("","Airway","","")
    

def test_title():
    ir.run_query("Gimme a Buck or I'll Touch You / Boilermaker","","","")
    

def test_no_hits():
    ir.run_query("","","","")

def test_multiple():
    ir.run_query("","","AWOL - A Way Of Life","Rock")


def main():
    #test_genre()
    #test_album()
    #test_author()
    #test_title()
    #test_no_hits()
    test_multiple()

main()