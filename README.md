# IMDB_Project

The DataMining project consists to retrieve all the information available from a website. The first aim of the project is to retrieve all the datas from the website choosen but also organize them and print it by a python code (furnished in the GitHub). 

Personal Project: 
We called the project IMDB as we wanted to scrap all the data from the website. 
First, please find the URL correponding to the Website : 
https://www.imdb.com/search/title/?genres=action&explore=title_type,genres&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=e0da8c98-35e8-4ebd-8e86-e7d39c92730c&pf_rd_r=3J0TPESRAX1XR8AZB553&pf_rd_s=center-2&pf_rd_t=15051&pf_rd_i=genre&ref_=ft_gnr_pr2_i_2
IMDb is the world's most popular and authoritative source for movie, TV and celebrity content. Find ratings and reviews for the newest movie and TV shows. 
We wanted to focus our only on the Action TV-Show and Movies. 

To retrieve and print the data you just need to run the python code after installing 2 packages (Requests and bs4). 
It will automatically give you the main information about each TV-Show and Movies : 
- Title
- Date
- Genre
- Resume
- Rating
- Actors
- Producers

We had some issues to retrieve some informations because they were stored in another URL. So we need to select the URL of each movies, enter in it and retrieve the additional datas. 
Alos, we wanted to have the datas for all Action movies, not only the one showed in the 1st page. We used the same logic as before to browse page by page automaticaly and print all the datas. 
