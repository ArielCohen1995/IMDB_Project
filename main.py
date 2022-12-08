import os
from web_scraping import *
from imdb_db import *
import argparse
import json


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('movie_or_tv', type=str, choices=['Movie', 'TV'], action='store', const='Movie', nargs='?')
    parser.add_argument('genre', type=str, choices=['Action', 'Comedy', 'Drama', 'Thriller', 'Adventure', 'Animation',
                                                    'Romance', 'Musical', 'Crime', 'All'], const='All', nargs='?',
                        help="Choose a genre.")
    parser.add_argument('year_beg', type=int, const=1, nargs='?')
    parser.add_argument('year_end', type=int, const=2022, nargs='?')
    return parser.parse_args()


if __name__ == '__main__':
    # This is the url from the action category in the website, but it could work for the other ones too.
    logging.basicConfig(filename=os.getcwd() + '/IMDB.log', encoding='utf-8', level=logging.INFO)

    with open('conf_IMDB.json') as json_config:
        config = json.load(json_config)
        url_action = config['URL_ACTION']
        url_comedy = config['URL_COMEDY']
        url_animation = config['URL_ANIMATION']
        url_thriller = config['URL_THRILLER']

    args = get_args()
    
    connection = pymysql.connect(user=config['USER'], password=config['PASSWORD'], host=config['HOST'])
    cursor = connection.cursor()
    cursor.execute("SHOW DATABASES LIKE 'IMDb_DB';")
    if cursor.fetchall() is None:
        init_DB()
        
    data_retrieving(args, url_action)
    logging.info('Finished')
