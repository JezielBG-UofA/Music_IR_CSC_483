'''
Authors: 
    Jeziel Banos Gonzalez
    []
    []
    []

File Description:

Instructions:


'''

class IRSystem:

    def __init__(self, file):
        pass


    def run_query(self, title, artist, members, genre):
        return self._run_query(title.lower().split(), artist.lower().split(), members.lower().split(), genre.lower().split())
    
    def _run_query(self, title, artist, members, genre):
        pass





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



