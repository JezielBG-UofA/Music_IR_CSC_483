from music_score_retrieval import IRSystem

def main(musicCollection):
    ir = IRSystem(musicCollection)

    while True:
        queryCheck = input("Please insert a music query. Press enter to continue, if you would like to exit, type \"exit\".")
        if queryCheck.upper() == "EXIT":
            break
        title = input("Please provide a title. If no title is desired, simply press ENTER on your keyboard.\n")
        artist = input("Please provide an artist. If no specific artist is desired, simply press ENTER on your keyboard.\n")
        album = input("Please provide an album. If no specific album is desired, simply press ENTER on your keyboard.\n")
        genre = input("Please provide a desired genre. Else press ENTER on your keyboard.\n")

        top_ten = ir.run_query(title, artist, album, genre)
        for i in range(0,len(top_ten)):
            print(f"{i+1}. {top_ten[i][0]} by artist {top_ten[i][1]} from album: {top_ten[i][2]}. Score: {top_ten[i][3]}")

main("./fma_metadata/trackData.csv")
