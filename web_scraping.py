import requests
import re
from bs4 import BeautifulSoup
from imdb_db import update_global_table


def check_item(movie_or_tv, year, genre, movie_or_tv_filter, genre_filter, year_beg_filter, year_end_filter):
    """Returns True if the movie passes the filter and False otherwise"""
    if movie_or_tv != movie_or_tv_filter:
        return False
    if genre_filter != 'All' and genre_filter not in genre:
        #print(genre)
        #print(genre_filter.split(','))
        return False
    if year < year_beg_filter or year > year_end_filter:
        return False
    return True


def get_cast(soup):
    """This function prints the casting of a movie/tv series including the actors and the directors, writers and
    creators. """
    production_team = []
    actors = []
    for child in soup.find('ul',
                           class_="ipc-metadata-list ipc-metadata-list--dividers-all title-pc-list "
                                  "ipc-metadata-list--baseAlt",
                           role="presentation").children:
        cat = child.contents[0].string
        if cat == 'Stars':
            content = child.div.ul.li
            while content:
                actor_id = int(''.join(c for c in content.a['href'] if c.isdigit()))
                actor = (content.a.string, actor_id)
                actors.append(actor)
                content = content.next_sibling
        else:
            content = child.div.ul.li
            while content:
                prod_id = int(''.join(c for c in content.a['href'] if c.isdigit()))
                prod = (content.a.string, prod_id, cat)
                production_team.append(prod)
                content = content.next_sibling

    return list(set(production_team)), list(set(actors))


def data_retrieving(args, my_url):
    """This function gets an URL from one of the categories of IMDB's website and prints each movie/tv show with
    relevant datas. """

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/102.0.0.0 Safari/537.36'}
    page = requests.get(my_url, headers=headers)
    assert page.status_code == 200
    while page:
        soup = BeautifulSoup(page.content, "html.parser")
        next_url = 'https://www.imdb.com' + soup.find(class_="desc").find_all('a')[-1]['href']
        movies_list = soup.find(class_="lister-list")

        movie = movies_list.find(class_="lister-item")
        while movie:
            title = movie.find(class_="lister-item-header").a.string
            movie_url = movie.find(class_="lister-item-header").a['href']
            movie_id = int(''.join(c for c in movie_url if c.isdigit()))
            genre = movie.find(class_="genre").string.strip().split(',')
            year = movie.find(class_='text-muted').string[1:-1]
            release_year = int(re.findall('[0-9]{4}', year)[0])
            if movie.strong:
                rating = float(movie.strong.string)
            else:
                rating = "NULL"
            resume = movie.find_all('p')[1].string
            if resume:
                resume = resume.strip()

            movie_page = requests.get('https://www.imdb.com' + movie_url, headers=headers)
            assert movie_page.status_code == 200
            movie_soup = BeautifulSoup(movie_page.content, "html.parser")

            if movie_soup.find(role="presentation", class_="ipc-inline-list__item", string="TV Series"):
                movie_or_tv = "TV"
            else:
                movie_or_tv = "Movie"

            if check_item(movie_or_tv, release_year, genre, args.movie_or_tv, args.genre, args.year_beg, args.year_end):
                prod, actors = get_cast(movie_soup)
                #print(title)
                #print(movie_id)
                #print(prod)
                #print(actors)
                #print("\n")
                update_global_table(movie_id, title, movie_or_tv, release_year, genre, rating, resume, prod, actors)


            movie = movie.next_sibling.next_sibling

        page = requests.get(next_url, headers=headers)
