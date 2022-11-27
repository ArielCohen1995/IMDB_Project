import pymysql

connection = pymysql.connect(user='root', password='Arielou95!', host='localhost')
cursor = connection.cursor()


def init_DB():
    """This function allows to create Databases"""
    try:
        #cursor.execute("DROP DATABASE IMDb_DB")
        #connection.commit()

        cursor.execute("CREATE DATABASE IMDb_DB")
        connection.commit()

        cursor.execute("CREATE TABLE IMDb_DB.global ("
                       "id INT PRIMARY KEY,"
                       "title VARCHAR(150),"
                       "type_input VARCHAR(150),"
                       "year_released INT,"
                       "rating REAL)")
        connection.commit()

        cursor.execute("CREATE TABLE IMDb_DB.genres ("
                       "movie_id INT ,"
                       "genre VARCHAR(150))")
        connection.commit()

        cursor.execute("CREATE TABLE IMDb_DB.synopsis ("
                       "movie_id INT ,"
                       "resume TEXT)")
        connection.commit()

        cursor.execute("CREATE TABLE IMDb_DB.actors ("
                       "id INT ,"
                       "movie_id INT ,"
                       "name VARCHAR(150))")
        connection.commit()

        cursor.execute("CREATE TABLE IMDb_DB.producers ("
                       "movie_id INT ,"
                       "id INT)")
        connection.commit()

        cursor.execute("CREATE TABLE IMDb_DB.producers_details ("
                       "id INT ,"
                       "work VARCHAR(150), "
                       "name VARCHAR(150))")
        connection.commit()

    except pymysql.err.InterfaceError:
        pass


def update_global_table(movie_id, title, movie_or_tv, release_year, genre, rating, resume, prod, actors):
    """This function allows to load the different tables from the web scrapping information retrieved"""
    try:
        cursor.execute("INSERT INTO IMDb_DB.global (id, title, type_input, year_released, rating) "
                       "VALUES (%s, %s, %s, %s, %s);", (movie_id, title, movie_or_tv, release_year, rating))
        connection.commit()

        for g in genre:
            cursor.execute("INSERT INTO IMDb_DB.genres (movie_id, genre) "
                           "VALUES (%s, %s);", (movie_id, g))
            connection.commit()

        cursor.execute("INSERT INTO IMDb_DB.synopsis (movie_id, resume) "
                       "VALUES (%s, %s);", (movie_id, resume))
        connection.commit()

        for actor in actors:
            cursor.execute("INSERT INTO IMDb_DB.actors (id, movie_id, name) "
                           "VALUES (%s, %s, %s);", (actor[1], movie_id, actor[0]))
        for staff in prod:
            cursor.execute("INSERT INTO IMDb_DB.producers (movie_id, id) "
                           "VALUES (%s, %s);", (movie_id, staff[1]))

            cursor.execute("INSERT INTO IMDb_DB.producers_details (id, work, name) "
                           "VALUES (%s, %s, %s);", (staff[1], staff[0], staff[2]))

    except pymysql.err.InterfaceError:
        pass

    except pymysql.err.IntegrityError:
        try:
            cursor.execute(
                "UPDATE IMDb_DB.global "
                "SET "
                "title = '%s',"
                "type_input = '%s',"
                "year_released = '%s',"
                "rating = '%s' "
                "WHERE id = '%s'", (title, movie_or_tv, release_year, rating, movie_id))

            for g in genre:
                cursor.execute(
                    "UPDATE IMDb_DB.genres "
                    "SET "
                    "genre = '%s'"
                    "WHERE movie_id = '%s'", (g, movie_id))

            cursor.execute(
                "UPDATE IMDb_DB.synopsis "
                "SET "
                "resume = '%s'"
                "WHERE movie_id = '%s'", (resume, movie_id))

            for actor in actors:
                cursor.execute(
                    "UPDATE IMDb_DB.actors "
                    "SET "
                    "name = '%s',"
                    "id = '%s'"
                    "WHERE movie_id = '%s'", (actor[0], actor[1], movie_id))

            for staff in prod:
                cursor.execute(
                    "UPDATE IMDb_DB.producers_details "
                    "SET "
                    "name = '%s',"
                    "id = '%s',"
                    "work = '%s'"
                    "WHERE movie_id = '%s'", (staff[0], staff[1], staff[2], movie_id))

                cursor.execute(
                    "UPDATE IMDb_DB.producers "
                    "SET "
                    "id = '%s'"
                    "WHERE movie_id = '%s'", (staff[1], movie_id))

        except pymysql.err.InterfaceError:
            pass

