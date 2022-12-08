# IMDB_Project KEVIN BENHAMOU & ARIEL COHEN

The DataMining project consists to retrieve all the information available from a website. The first aim of the project is to retrieve all the datas from the website choosen but also organize them and print it by a python code (furnished in the GitHub). 

Personal Project: 
We called the project IMDB as we wanted to scrap all the data from the website. 
First, please find the URL correponding to the Website : 
https://www.imdb.com/search/title/?genres=action&explore=title_type,genres&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=e0da8c98-35e8-4ebd-8e86-e7d39c92730c&pf_rd_r=3J0TPESRAX1XR8AZB553&pf_rd_s=center-2&pf_rd_t=15051&pf_rd_i=genre&ref_=ft_gnr_pr2_i_2
IMDb is the world's most popular and authoritative source for movie, TV and celebrity content. Find ratings and reviews for the newest movie and TV shows. 
We wanted to focus our only on the Action TV-Show and Movies. 

To retrieve and print the data you just need to run the python code after installing 2 packages (Requests and bs4). Please refer to the requirement.txt for that. 
It will automatically give you the main information about each TV-Show and Movies : 
- Title
- Date
- Genre
- Resume
- Rating from IMBD
- Actors
- Producers
- Rating from Rotten Tomatoes
- Rating from Metacritics

About the rating from Rotten Tomatoes and Metatrics, we used the OMDB API to have this information. The goal was to compare the rating between the different website and then different users. About the connection to the API, you need to ask an API key to connect by yourself and have access to the data. 
The way to modify the information will be explained later in the session "How to run the code". 

We had some issues to retrieve some informations because they were stored in another URL. So we need to select the URL of each movies, enter in it and retrieve the additional datas. 
Alos, we wanted to have the datas for all Action movies, not only the one showed in the 1st page. We used the same logic as before to browse page by page automaticaly and print all the datas. 

![Diagram_IMDB_DB](https://user-images.githubusercontent.com/116627393/206470563-4c4f6c80-b528-43ac-bac7-95d6c75749c9.png)


The IMBD Databases contains several tables: 
- Global : where we stock the main information about the Movies, TV-Shows, ...
- Genres : where we stock the genre of each movies
- Synopsis : where we stock the resume of each movies
- Actors : where we stock the actors of each movies
- Actors_Detail : where we stock the actors id and name
- Producers : where we stock the staffing id of each movies
- Producers_Details : where we stock the works, names, id of each producer 

Please find above in the diagram the link between each table of the IMDB Database. 

HOW TO RUN THE CODE: 
You need have all the python files loaded in the same folder beause each file will allow you to run a part of the project:
- main.py :
  * give you the possibility to ask to website the information that you want :
    ** You need to choice if you want Movie or TV_Show, from which category (Action, Comedy, ...), from which year (2010) until which year (2022) 
    ** Then you need to run the parse by giving the information as defined (example : TV Comedy 2010 2022) 
    ** By default it will select the Movie from All the categories from the beggining to 2022
  * We will grew up the number of possibilities further with more categories and more type of input (Games, Musics, ...) 
  
 - web_scraping.py:
  * it will scrapp the website given the information that you ask from the argparse in the main.py file. 
  * you can check the python file to have more information about the different functions developed and used
  
 - imdb_db.py:
  * it allows to create the Database as decribed above and load the data during the scrapping 
  * it allows also to update the information from the datas retrieved into the DB. for example, if the rating is updated on a movie, it will update the information about the movie, not create a new line or delete and create new one. 
  
 - conf_IMDB.json:
    * The JSON file stores all the information that is needed about the different URL that can be used 
    * You need to update the USERNAME, PASSWORD and HOSTNAME for SQL connection.
    * You need to update your own API_KEY to retrieve the information from the OMDB API. 
 
  


