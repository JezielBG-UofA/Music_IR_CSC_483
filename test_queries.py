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

def testPrinter(results):
    for i in range(0,len(results)):
        print(f"{i+1}. {results[i][0]} by artist {results[i][1]} from album {results[i][2]}. Score: {results[i][3]}")



def test_genre():
    print("====TESTING GENRE====")
    print('Testing Genre \'Pop\':')
    results = ir.run_query("","","","Pop")
    testPrinter(results)
    print('------------------------------------------')

    print('Testing Genre \'Deep Funk\'. Only one Deep Funk song exists in database.')
    results = ir.run_query("", "", "", "Deep Funk")
    #assert("San Fran Interlude (Edit)" in results)
    testPrinter(results)
    print('------------------------------------------')
    print('==========================================')
    

def test_album():
    print("====TESTING WITH ALBUM TITLE \"AWOL - A Way of Life\"====")
    print('Exact album title match.')
    results = ir.run_query("","","AWOL - A Way Of Life","")
    assert([x[2].lower() for x in results[:6]] == ["awol - a way of life"]*6)
    testPrinter(results)
    print('------------------------------------------')

    print('Lowercase exact title query.')
    results = ir.run_query("", "", "awol - a way of life", "")
    assert([x[2].lower() for x in results[:6]] == ["awol - a way of life"]*6)
    testPrinter(results)
    print('------------------------------------------')
    
    print("Ommision of '-'")
    results = ir.run_query("", "", "awol a way of life", "")
    assert([x[2].lower() for x in results[:6]] == ["awol - a way of life"]*6)
    testPrinter(results)
    print('------------------------------------------')
    
    print('Partial title of "AWOL - A Way of Life" using "a way of life"')
    results = ir.run_query("", "", "a way of life", "")
    assert([x[2].lower() for x in results[:6]] == ["awol - a way of life"]*6)
    testPrinter(results)
    print('------------------------------------------')

    print('Partial title of "AWOL - A Way of Life" using "awol"')
    results = ir.run_query("", "", "awol", "")
    assert([x[2].lower() for x in results[:6]] == ["awol - a way of life"]*6)
    testPrinter(results)
    print('------------------------------------------')
    print('==========================================')
    

def test_author():
    print("====TESTING WITH ARTIST NAME \"Airway\"====")
    print('Exact artist name match:')
    results = ir.run_query("","Airway","","")
    assert([x[1].lower() for x in results[:3]] == ["airway"]*3)
    testPrinter(results)
    print('------------------------------------------')

    print('Lowercase artist name match:')
    results = ir.run_query("", "airway", "", "")
    assert([x[1].lower() for x in results[:3]] == ["airway"]*3)
    testPrinter(results)
    print('------------------------------------------')
    print('==========================================')

    print("====TESTING WITH ARTIST NAME \"Food For Animals\"")
    print('Exact artist name match:')
    results = ir.run_query("", "Food For Animals", "", "")
    assert([x[1].lower() for x in results[:4]] == ["food for animals"]*4)
    testPrinter(results)
    print('------------------------------------------')

    print('Lowercase artist name match:')
    results = ir.run_query("", "food for animals", "", "")
    assert([x[1].lower() for x in results[:4]] == ["food for animals"]*4)
    testPrinter(results)
    print('------------------------------------------')

    print('Partial name match "food for":')
    results = ir.run_query("", "food for", "", "")
    assert("food for animals" in [x[1].lower() for x in results])
    testPrinter(results)
    print('------------------------------------------')

    print('Partial name match "animals food":')
    results = ir.run_query("", "animals food", "", "")
    assert("food for animals" in [x[1].lower() for x in results])
    testPrinter(results)
    print('------------------------------------------')

    print('Partial name match "for animals":')
    results = ir.run_query("", "for animals", "", "")
    assert("food for animals" in [x[1].lower() for x in results])
    testPrinter(results)
    print('------------------------------------------')

    # No query for partial name match "animals" as Rational Animals artist is more important in terms of scoring.
    print('==========================================')
    

def test_title():
    print("====TESTING WITH TITLE \"Gimme a Buck or I'll Touch You / Boilermaker\"====")
    print("Testing with full title:")
    results = ir.run_query("Gimme a Buck or I'll Touch You / Boilermaker", "", "", "")
    assert(results[0][0].lower() == "gimme a buck or i'll touch you / boilermaker")
    testPrinter(results)
    print('------------------------------------------')

    print("Testing with lowercase title:")
    results = ir.run_query("gimme a buck or i'll touch you / boilermaker", "", "", "")
    assert(results[0][0].lower() == "gimme a buck or i'll touch you / boilermaker")
    testPrinter(results)
    print('------------------------------------------')

    print("Testing partial title \"gimme a buck or i'll touch you\":")
    results = ir.run_query("gimme a buck or i'll touch you", "", "", "")
    assert(results[0][0].lower() == "gimme a buck or i'll touch you / boilermaker")
    testPrinter(results)
    print('------------------------------------------')

    print("Testing partial title \"boilermaker\":")
    results = ir.run_query("boilermaker", "", "", "")
    assert(results[0][0].lower() == "gimme a buck or i'll touch you / boilermaker")
    testPrinter(results)
    print('------------------------------------------')
    print('==========================================')
    

def test_no_hits():
    print("====TESTING QUERIES WITH NO HITS (Treat result set of blank query as baseline.)====" \
    "\nAll should return order based on # of listens.")
    print('Testing with blank input:')
    noHits = ir.run_query("","","","")
    testPrinter(noHits)
    print('------------------------------------------')
    
    print('Testing with nonexistent string "hejdlzo"')
    results = ir.run_query("hejdlzo", "hejdlzo", "hejdlzo", "hejdlzo")
    assert(results == noHits)
    testPrinter(results)
    print('------------------------------------------')
    '''
    print('Testing with nonexistent string "hejdlzo" as subset of inputs, leaving others empty.' \
    '\nIntuition: If nonexistent string in each individual slot doesn\'t change score, no combination of them will alter score:')
    assert(ir.run_query("hejdlzo", "", "", "") == noHits)
    assert(ir.run_query("", "hejdlzo", "", "") == noHits)
    assert(ir.run_query("", "", "hejdlzo", "") == noHits)
    assert(ir.run_query("", "", "", "hejdlzo") == noHits)
    print('Success. No non-noHit value found.')
    print('------------------------------------------')
    print('==========================================')
    '''

def test_multiple():
    testPrinter(ir.run_query("","","AWOL - A Way Of Life","Rock"))


def main():
    #test_genre()
    #test_album()
    #test_author()
    test_title()
    #test_no_hits()
    #test_multiple()

main()