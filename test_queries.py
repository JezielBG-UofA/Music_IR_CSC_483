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

    print('Testing Genre \'Deep Funk\'. Only one Deep Funk song exists in database:')
    results = ir.run_query("", "", "", "Deep Funk")
    testPrinter(results)
    assert("San Fran Interlude (Edit)" in results[0])
    print('------------------------------------------')

    print('Testing Genre \'bollywood\'. No songs under \'bollywood\' genre should exist:')
    results = ir.run_query("", "", "", "bollywood")
    testPrinter(results)
    assert(results == ir.run_query("", "", "", ""))
    print('------------------------------------------')

    print('Testing Genre \'historic\' and \'old time\'. Should return same result set:')
    results = ir.run_query("", "", "", "historic")
    testPrinter(results)
    assert(results == ir.run_query("", "", "", "old time"))
    print('------------------------------------------')

    print('Testing Genre \'alTER native --- hip..hop\'. Should return result set for genre \'alternative hiphop\':')
    results = ir.run_query("", "", "", "alTER native --- hip..hop")
    testPrinter(results)
    assert(results == ir.run_query("", "", "", "alternative hiphop"))
    print('------------------------------------------')

    print('==========================================')
    

def test_album():
    print("====TESTING WITH ALBUM TITLE \"AWOL - A Way of Life\"====")
    print('Exact album title match.')
    results = ir.run_query("","","AWOL - A Way Of Life","")
    testPrinter(results)
    assert([x[2].lower() for x in results[:6]] == ["awol - a way of life"]*6)
    print('------------------------------------------')

    print('Lowercase exact title query.')
    results = ir.run_query("", "", "awol - a way of life", "")
    testPrinter(results)
    assert([x[2].lower() for x in results[:6]] == ["awol - a way of life"]*6)
    print('------------------------------------------')
    
    print("Ommision of '-'")
    results = ir.run_query("", "", "awol a way of life", "")
    testPrinter(results)
    assert([x[2].lower() for x in results[:6]] == ["awol - a way of life"]*6)
    print('------------------------------------------')
    
    print('Partial title of "AWOL - A Way of Life" using "a way of life"')
    results = ir.run_query("", "", "a way of life", "")
    testPrinter(results)
    assert([x[2].lower() for x in results[:6]] == ["awol - a way of life"]*6)
    print('------------------------------------------')

    print('Partial title of "AWOL - A Way of Life" using "awol"')
    results = ir.run_query("", "", "awol", "")
    testPrinter(results)
    assert([x[2].lower() for x in results[:6]] == ["awol - a way of life"]*6)
    print('------------------------------------------')
    print('==========================================')
    

def test_author():
    print("====TESTING WITH ARTIST NAME \"Airway\"====")
    print('Exact artist name match:')
    results = ir.run_query("","Airway","","")
    testPrinter(results)
    assert([x[1].lower() for x in results[:3]] == ["airway"]*3)
    print('------------------------------------------')

    print('Lowercase artist name match:')
    results = ir.run_query("", "airway", "", "")
    testPrinter(results)
    assert([x[1].lower() for x in results[:3]] == ["airway"]*3)
    print('------------------------------------------')
    print('==========================================')

    print("====TESTING WITH ARTIST NAME \"Food For Animals\"")
    print('Exact artist name match:')
    results = ir.run_query("", "Food For Animals", "", "")
    testPrinter(results)
    assert([x[1].lower() for x in results[:4]] == ["food for animals"]*4)
    print('------------------------------------------')

    print('Lowercase artist name match:')
    results = ir.run_query("", "food for animals", "", "")
    testPrinter(results)
    assert([x[1].lower() for x in results[:4]] == ["food for animals"]*4)
    print('------------------------------------------')

    print('Partial name match "food for":')
    results = ir.run_query("", "food for", "", "")
    testPrinter(results)
    assert("food for animals" in [x[1].lower() for x in results])
    print('------------------------------------------')

    print('Partial name match "animals food":')
    results = ir.run_query("", "animals food", "", "")
    testPrinter(results)
    assert("food for animals" in [x[1].lower() for x in results])
    print('------------------------------------------')

    print('Partial name match "for animals":')
    results = ir.run_query("", "for animals", "", "")
    testPrinter(results)
    assert("food for animals" in [x[1].lower() for x in results])
    print('------------------------------------------')

    # No query for partial name match "animals" as Rational Animals artist is more important in terms of scoring.
    print('Partial name match "animals" (looking for artist \'Rational Animals\'):')
    results = ir.run_query("", "animals", "", "")
    testPrinter(results)
    assert("rational animals" in [x[1].lower() for x in results])
    print('------------------------------------------')
    print('==========================================')
    

def test_title():
    print("====TESTING WITH TITLE \"Gimme a Buck or I'll Touch You / Boilermaker\"====")
    print("Testing with full title:")
    results = ir.run_query("Gimme a Buck or I'll Touch You / Boilermaker", "", "", "")
    testPrinter(results)
    assert(results[0][0].lower() == "gimme a buck or i'll touch you / boilermaker")
    print('------------------------------------------')

    print("Testing with lowercase title:")
    results = ir.run_query("gimme a buck or i'll touch you / boilermaker", "", "", "")
    testPrinter(results)
    assert(results[0][0].lower() == "gimme a buck or i'll touch you / boilermaker")
    print('------------------------------------------')

    print("Testing partial title \"gimme a buck or i'll touch you\":")
    results = ir.run_query("gimme a buck or i'll touch you", "", "", "")
    testPrinter(results)
    assert(results[0][0].lower() == "gimme a buck or i'll touch you / boilermaker")
    print('------------------------------------------')

    print("Testing partial title \"boilermaker\":")
    results = ir.run_query("boilermaker", "", "", "")
    testPrinter(results)
    assert(results[0][0].lower() == "gimme a buck or i'll touch you / boilermaker")
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
    testPrinter(results)
    assert(results == noHits)
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
    print('===TESTING QUERIES BASED ON MULTIPLE INPUTS===')
    print('Testing with album \'AWOL - A Way of Life\' and genre \'Hip-Hop\':')
    results = ir.run_query("","","AWOL - A Way Of Life","Hip-Hop")
    testPrinter(results)
    assert([x[2].lower() for x in results[:6]] == ["awol - a way of life"]*6)
    print('------------------------------------------')

    print('Testing with album \'AWOL - A Way of Life.\' and genre \'Christmas\' '
    '(album weight should outweight genre):')
    results = ir.run_query("","","AWOL - A Way Of Life","Christmas")
    testPrinter(results)
    assert("awol - a way of life" in [x[2].lower() for x in results])
    print('------------------------------------------')

    print('Testing with title \'Odd Number One\' and album \'AWOL - A Way of Life\' '
    '(title must outweigh album):')
    results = ir.run_query("Odd Number One","","AWOL - A Way Of Life","")
    testPrinter(results)
    assert("odd number one" == results[0][0].lower())
    print('------------------------------------------')
    print('==========================================')


def main():
    test_genre()
    test_album()
    test_author()
    test_title()
    test_no_hits()
    test_multiple()

main()