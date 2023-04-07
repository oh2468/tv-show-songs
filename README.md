# TV Show Songs

## Description

An app used to search (scrape) for the songs used in various tv shows/episodes from the most popular tv show music website. The info is then saved in a database that can also be exported to a csv file. The songs found on the website have a corresponding url that contains the song url at Spotify. The first link is stored in the local database and can at a later time be updated to the corresponding Spotify url and replaced in the local database.

Precautions are taken when scraping the site for the episodes and their songs, basically requests/second. Be warned though, since I don't have control over how the website monitors and controls their web traffic you risk getting banned/blocked from using their site all togther when using this app. Another precaution is that you can select to scrape a single seasons for its songs so that you don't have to scrape entire shows and possibly their 300+ episodes.

You can also use the app to browse (print to console) the local database with the currently scraped shows/seasons/episodes/songs. And if you feel like removing something from the database (in case you want to update the show) you can also delete things with the app. The database can also be exported to a csv file, just in case you want an easier time browsing the data and lack a dataabse manager that can open/read sql files. 

## Getting Started

Download all the dependecies, then run the app from a terminal e.g.: ```python app.py```

### Dependencies

* Python (developed with v. 3.10.5)
* SQLite3 (developed with v. 2.6.0)
* Requests (developed with v. 2.28.2)
* SQLAlchemy (developed with v. 2.0.4)

