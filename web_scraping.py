import requests
import re
from bs4 import BeautifulSoup
from imdb_db import update_global_table
import json
import ast
import logging


def check_item(movie_or_tv, year, genre, movie_or_tv_filter, genre_filter, year_beg_filter, year_end_filter):
    """Returns True if the movie passes the filter and False otherwise"""
    if movie_or_tv != movie_or_tv_filter:
        return False
    if genre_filter != 'All' and genre_filter not in genre:
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


def get_movie_data(movie, args, headers, api_key):
    """This function allows to retrieve the data from the web"""
    title = movie.find(class_="lister-item-header").a.string
    movie_url = movie.find(class_="lister-item-header").a['href']
    omdb_id = movie_url.split('/')[2]
    movie_id = int(''.join(c for c in movie_url if c.isdigit()))
    genre = movie.find(class_="genre").string.strip().split(',')
    year = movie.find(class_='text-muted').string[1:-1]
    release_year = int(re.findall('[0-9]{4}', year)[0])
    if movie.strong:
        rating = float(movie.strong.string)
    else:
        rating = None
    resume = movie.find_all('p')[1].string
    if resume:
        resume = resume.strip()

    movie_page = requests.get('https://www.imdb.com' + movie_url, headers=headers)

    if movie_page.status_code != 200:
        logging.error("URL doesn't exist ! Failed")

    movie_soup = BeautifulSoup(movie_page.content, "html.parser")

    if movie_soup.find(role="presentation", class_="ipc-inline-list__item", string="TV Series"):
        movie_or_tv = "TV"
    else:
        movie_or_tv = "Movie"

    if check_item(movie_or_tv, release_year, genre, args.movie_or_tv, args.genre, args.year_beg, args.year_end):
        prod, actors = get_cast(movie_soup)
        rotten_rating, meta_rating = get_ratings(omdb_id, api_key)

        return movie_id, title, movie_or_tv, release_year, genre, rating, resume, prod, actors, rotten_rating, meta_rating
    else:
        return None


def get_ratings(movie_id, api_key):
    omdb_url = 'http://www.omdbapi.com/?apikey=' + api_key + '&i=' + movie_id
    page = requests.get(omdb_url)
    if page.status_code != 200:
        logging.error("URL doesn't exist ! Failed")
    movie_json = page.json()
    if movie_json['Ratings'] != []:
        rotten_rating = movie_json['Ratings'][1]['Value']
        meta_rating = movie_json['Ratings'][2]['Value']
        rotten_rating = float(rotten_rating.split('%')[0])/10
        meta_rating = float(meta_rating.split('/')[0])/10
    else:
        rotten_rating = None
        meta_rating = None

    return rotten_rating, meta_rating


def data_retrieving(args, my_url):
    """This function gets an URL from one of the categories of IMDB's website and prints each movie/tv show with
    relevant datas. """
    with open('conf_IMDB.json') as json_config:
        config = json.load(json_config)
        headers = ast.literal_eval(config['HEADERS'])
        api_key = config['API_KEY']

    page = requests.get(my_url, headers=headers)

    if page.status_code != 200:
        logging.error("URL doesn't exist ! Failed")

    while page:
        soup = BeautifulSoup(page.content, "html.parser")
        next_url = 'https://www.imdb.com' + soup.find(class_="desc").find_all('a')[-1]['href']
        movies_list = soup.find(class_="lister-list")

        movie = movies_list.find(class_="lister-item")
        while movie:
            data = get_movie_data(movie, args, headers, api_key)
            if data:
                update_global_table(*data)
                logging.info(f'Retrieving movie :{data[1]}')
            movie = movie.next_sibling.next_sibling

        page = requests.get(next_url, headers=headers)