import requests
import re
from bs4 import BeautifulSoup
from urllib.request import urlopen


class Movie:

    def __init__(self, title, movie_or_tv, year, rating, genre, actors, resume, producers):
        self.title = title
        self.movie_or_tv = movie_or_tv
        self.year = year
        self.rating = rating
        self.genre = genre
        self.actors = actors
        self.resume = resume
        self.producers = producers


def print_cast(soup):
    for child in soup.find('ul',
                                 class_="ipc-metadata-list ipc-metadata-list--dividers-all title-pc-list ipc-metadata-list--baseAlt",
                                 role="presentation").children:
        print(child.contents[0].string)
        content = child.div.ul.li
        while content:
            print(content.a.string)
            content = content.next_sibling


def data_retrieving(url):
    page = requests.get(url)
    assert page.status_code == 200

    while page:
        soup = BeautifulSoup(page.content, "html.parser")
        next_url = 'https://www.imdb.com' + soup.find(class_="desc").find_all('a')[-1]['href']
        movies_list = soup.find(class_="lister-list")

        movie = movies_list.find(class_="lister-item")
        while movie:
            title = movie.find(class_="lister-item-header").a.string
            movie_url = movie.find(class_="lister-item-header").a['href']
            genre = movie.find(class_="genre").string.strip()
            year = movie.find(class_='text-muted').string[1:-1]
            if movie.strong:
                rating = movie.strong.string
            else:
                rating = "NOT RELEASED"
            resume = movie.find_all('p')[1].string
            if resume:
                resume = resume.strip()


            movie_page = requests.get( 'https://www.imdb.com' + movie_url)
            assert movie_page.status_code == 200
            movie_soup = BeautifulSoup(movie_page.content, "html.parser")


            if movie_soup.find(role="presentation", class_="ipc-inline-list__item", string="TV Series"):
                movie_or_tv = "TV Series"
            else:
                movie_or_tv = "Movie"

            #### BUG IS HERE
            #for child in movie_soup.find_all('div', class_="nas-slot")[4].next_sibling.next_sibling:
            #    print(child)

            print("TITLE: ", title)
            print(movie_or_tv)
            print("Released in: ", year)
            print("Genre: ", genre)
            print("Rating: ", rating)
            print("Synopsis: ", resume)
            print_cast(movie_soup)
            print("\n")

            #gets the movie url, load it then get the actors, producers, and resume
            movie = movie.next_sibling.next_sibling

        page = requests.get(next_url)



    return 'ok'


url = "https://www.imdb.com/search/title/?genres=action&explore=title_type,genres&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=e0da8c98-35e8-4ebd-8e86-e7d39c92730c&pf_rd_r=HH27WYBNND88H4C8FJ15&pf_rd_s=center-2&pf_rd_t=15051&pf_rd_i=genre&ref_=ft_gnr_pr2_i_2"
print(data_retrieving(url))