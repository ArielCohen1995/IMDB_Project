import pymysql
import json


def check_DB_exist():
    """This function allows to check if the Databases already exist or not"""
    with open('conf_IMDB.json') as json_config:
        config = json.load(json_config)
        connection = pymysql.connect(user=config['USER'], password=config['PASSWORD'], host=config['HOST'])
        cursor = connection.cursor()
        cursor.execute("SHOW DATABASES LIKE 'ariel_kevin';")

    if not cursor.fetchall():
        return False
    else:
        return True


def init_DB():
    """This function allows to create Databases"""
    with open('conf_IMDB.json') as json_config:
        config = json.load(json_config)
        connection = pymysql.connect(user=config['USER'], password=config['PASSWORD'], host=config['HOST'])
        cursor = connection.cursor()

        cursor.execute("CREATE DATABASE ariel_kevin")
        connection.commit()


def create_table_global():
    """Creates table global"""
    with open('conf_IMDB.json') as json_config:
        config = json.load(json_config)
        connection = pymysql.connect(user=config['USER'], password=config['PASSWORD'], host=config['HOST'])
        cursor = connection.cursor()

        query = """
                CREATE TABLE IF NOT EXISTS ariel_kevin.global (
                id INT PRIMARY KEY,
                title VARCHAR(150),
                type_input VARCHAR(150),
                year_released INT,
                rating_IMDB REAL,
                rating_Rot_To REAL,
                rating_Metacritic REAL
                );
                """
        cursor.execute(query)
        connection.commit()


def create_table_genre():
    """Creates table genre"""
    with open('conf_IMDB.json') as json_config:
        config = json.load(json_config)
        connection = pymysql.connect(user=config['USER'], password=config['PASSWORD'], host=config['HOST'])
        cursor = connection.cursor()

        query = """
                CREATE TABLE IF NOT EXISTS ariel_kevin.genres (
                    movie_id INT,
                    genre VARCHAR(150)
                );
        """
        cursor.execute(query)
        connection.commit()


def create_table_synopsis():
    """Creates table synopsis"""
    with open('conf_IMDB.json') as json_config:
        config = json.load(json_config)
        connection = pymysql.connect(user=config['USER'], password=config['PASSWORD'], host=config['HOST'])
        cursor = connection.cursor()

        query = """
                CREATE TABLE IF NOT EXISTS ariel_kevin.synopsis (
                    movie_id INT PRIMARY KEY,
                    resume TEXT
                );
        """
        cursor.execute(query)
        connection.commit()


def create_table_actors():
    """Creates table actors"""
    with open('conf_IMDB.json') as json_config:
        config = json.load(json_config)
        connection = pymysql.connect(user=config['USER'], password=config['PASSWORD'], host=config['HOST'])
        cursor = connection.cursor()

        query = """
                CREATE TABLE IF NOT EXISTS ariel_kevin.actors (
                    id INT ,
                    movie_id INT
                );
        """
        cursor.execute(query)
        connection.commit()


def create_table_actors_details():
    """Creates table actors_details"""
    with open('conf_IMDB.json') as json_config:
        config = json.load(json_config)
        connection = pymysql.connect(user=config['USER'], password=config['PASSWORD'], host=config['HOST'])
        cursor = connection.cursor()

        query = """
                CREATE TABLE IF NOT EXISTS ariel_kevin.actors_details (
                    id INT PRIMARY KEY,
                    name VARCHAR(150)
                );
        """
        cursor.execute(query)
        connection.commit()


def create_table_producers():
    """Creates table producers"""
    with open('conf_IMDB.json') as json_config:
        config = json.load(json_config)
        connection = pymysql.connect(user=config['USER'], password=config['PASSWORD'], host=config['HOST'])
        cursor = connection.cursor()

        query = """
                CREATE TABLE IF NOT EXISTS ariel_kevin.producers (
                    movie_id INT,
                    id INT ,
                    work VARCHAR(150)
                );
                """
        cursor.execute(query)
        connection.commit()


def create_table_producers_details():
    """Creates table producers_details"""
    with open('conf_IMDB.json') as json_config:
        config = json.load(json_config)
        connection = pymysql.connect(user=config['USER'], password=config['PASSWORD'], host=config['HOST'])
        cursor = connection.cursor()

        query = """
                CREATE TABLE IF NOT EXISTS ariel_kevin.producers_details (
                    id INT PRIMARY KEY,
                    name VARCHAR(150)
                );
        """
        cursor.execute(query)
        connection.commit()


def update_global_table(movie_id, title, movie_or_tv, release_year, genre, rating_IMDB, resume, prod, actors,
                        rating_Rot_To, rating_Metacritic):
    """This function allows to load the different tables from the web scrapping information retrieved"""
    with open('conf_IMDB.json') as json_config:
        config = json.load(json_config)
        connection = pymysql.connect(user=config['USER'], password=config['PASSWORD'], host=config['HOST'])
        cursor = connection.cursor()

    try:
        cursor.execute(
            "INSERT INTO ariel_kevin.global (id, title, type_input, year_released, rating_IMDB, rating_Rot_To, "
            "rating_Metacritic) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s);",
            (movie_id, title, movie_or_tv, release_year, rating_IMDB, rating_Rot_To, rating_Metacritic))
        connection.commit()

        for g in genre:
            cursor.execute("INSERT INTO ariel_kevin.genres (movie_id, genre) "
                           "VALUES (%s, %s);", (movie_id, g))
            connection.commit()

        cursor.execute("INSERT INTO ariel_kevin.synopsis (movie_id, resume) "
                       "VALUES (%s, %s);", (movie_id, resume))
        connection.commit()

        for actor in actors:
            cursor.execute("INSERT INTO ariel_kevin.actors (id, movie_id) "
                           "VALUES (%s, %s);", (actor[1], movie_id))

            cursor.execute("INSERT INTO ariel_kevin.actors_details (id, name) "
                           "VALUES (%s, %s);", (actor[1], actor[0]))

        for staff in prod:
            cursor.execute("INSERT INTO ariel_kevin.producers (movie_id, id, work) "
                           "VALUES (%s, %s, %s);", (movie_id, staff[1], staff[2]))

            cursor.execute("INSERT INTO ariel_kevin.producers_details (id, name) "
                           "VALUES (%s, %s);", (staff[1], staff[0]))

    except pymysql.err.IntegrityError:
        cursor.execute(
            "UPDATE ariel_kevin.global "
            "SET "
            "title = %s, "
            "type_input = %s, "
            "year_released = %s, "
            "rating_IMDB = %s, "
            "rating_Rot_To = %s, "
            "rating_Metacritic = %s "
            "WHERE id = %s",
            (title, movie_or_tv, release_year, rating_IMDB, rating_Rot_To, rating_Metacritic, movie_id))
        connection.commit()

        cursor.execute(
            "UPDATE ariel_kevin.synopsis "
            "SET "
            "resume = %s "
            "WHERE movie_id = %s", (resume, movie_id))
        connection.commit()

        for actor in actors:
            cursor.execute(
                "UPDATE ariel_kevin.actors_details "
                "SET "
                "name = %s "
                "WHERE id = %s", (actor[0], actor[1]))
            connection.commit()

        for staff in prod:
            cursor.execute(
                "UPDATE ariel_kevin.producers_details "
                "SET "
                "name = %s "
                "WHERE id = %s", (staff[0], staff[1]))
            connection.commit()

