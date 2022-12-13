import os
from web_scraping import *
from imdb_db import *
import argparse
import json


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('movie_or_tv', type=str, choices=['Movie', 'TV'], action='store', const='Movie', default='Movie', nargs='?')
    parser.add_argument('genre', type=str, choices=['Action', 'Comedy', 'Drama', 'Thriller', 'Adventure', 'Animation',
                                                    'Romance', 'Musical', 'Crime', 'All'], const='All', nargs='?',
                        default='All', help="Choose a genre.")
    parser.add_argument('year_beg', type=int, const=1, nargs='?', default=1)
    parser.add_argument('year_end', type=int, const=2022, nargs='?', default=2022)
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

    if not check_DB_exist():
        init_DB()

    create_table_global()
    create_table_genre()
    create_table_synopsis()
    create_table_actors()
    create_table_actors_details()
    create_table_producers()
    create_table_producers_details()

    data_retrieving(args, url_action)
    logging.info('Finished')
