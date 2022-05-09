from luscious_dl import album
import random
try:
    from helpers import Logger
except:
    from .helpers import Logger

Album = album.Album


class Luscious:
    def __init__(self, search_query: str='', sorting: str = 'date_trending', page: int = 1, max_pages: int = 1, max_resuts=5):
        self.max_resuts = max_resuts
        self.album = None
        self.logger = Logger('luscious')
        if search_query != '':
            self.search(search_query, sorting, page, max_pages)

    def get_results(self):
        message = "Results: \n"
        for result in self.results:
            # print(result)
            msg = "\nID: " + result.id_
            msg += "\nTitle: " + result.title
            msg += "\nPictures: " + str(result.number_of_pictures)
            msg += "\nGifs: " + str(result.number_of_animated_pictures)
            message += msg + "\n"
        return message

    def search(self, search_query: str, sorting: str = 'date_trending', page: int = 1, max_pages: int = 1) -> list[Album]:
        self.logger.info(f'Searching albums with keyword: {search_query} | Page: {page} | Max pages: {max_pages} | Sort: {sorting}')
        self.results = album.search_albums(search_query, sorting, page, max_pages)[:self.max_resuts]
        # [(result.fetch_info(), result.fetch_pictures()) for result in self.results]
        return self.results

    def get_random(self):
        selected = random.choice(self.results)
        selected.fetch_info()
        selected.fetch_pictures()
        return {
            "title": selected.title,
            "total": selected.number_of_pictures
            + selected.number_of_animated_pictures,
            "images": selected.pictures
        }

    def get_albuns(self):
        return (self.get_results(), self.results)

    def fetch_from_id(self, id_):
        album = Album(id_)
        album.fetch_info()
        album.fetch_pictures()
        return album


if __name__ == "__main__":
    print(Luscious("marvel").get_results())
