from web_scraping import *
from imdb_db import *
import argparse


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
    url_action = "https://www.imdb.com/search/title/?genres=action&explore=title_type," \
                 "genres&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=e0da8c98-35e8-4ebd-8e86-e7d39c92730c&pf_rd_r=B71GWDC6Q6WC6SMR636X" \
                 "&pf_rd_s=center-2&pf_rd_t=15051&pf_rd_i=genre&ref_=ft_gnr_pr2_i_2"

    url_comedy = "https://www.imdb.com/search/title/?genres=comedy&explore=title_type," \
                 "genres&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=3396781f-d87f-4fac-8694-c56ce6f490fe&pf_rd_r=EAQXV52SP0W48QTA0JWN" \
                 "&pf_rd_s=center-1&pf_rd_t=15051&pf_rd_i=genre&ref_=ft_gnr_pr1_i_1 "

    url_animation = "https://www.imdb.com/search/title/?genres=animation&explore=title_type," \
                    "genres&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=fd0c0dd4-de47-4168-baa8-239e02fd9ee7&pf_rd_r" \
                    "=EAQXV52SP0W48QTA0JWN&pf_rd_s=center-4&pf_rd_t=15051&pf_rd_i=genre&ref_=ft_gnr_pr4_i_1 "

    url_thriller = "https://www.imdb.com/search/title/?genres=thriller&explore=title_type," \
                   "genres&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=e0da8c98-35e8-4ebd-8e86-e7d39c92730c&pf_rd_r" \
                   "=4BX7TC2D2K8A04FSEZAN&pf_rd_s=center-2&pf_rd_t=15051&pf_rd_i=genre&ref_=ft_gnr_pr2_i_3 "

    args = get_args()
    init_DB()
    data_retrieving(args, url_action)