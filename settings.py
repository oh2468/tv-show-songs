# scraping variables to adjust delay interval
SCRAPE_DELAY_MIN = 1.0
SCRAPE_DELAY_MAX = 3.0

# settings used in the requests header
MY_USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9"

# base urls to tunefind used to build further paths
BASE_URL = "https://www.tunefind.com"
BASE_URL_SHOW = BASE_URL + "/show/{show_name}"
BASE_URL_API = BASE_URL + "/api/frontend"

# api paths to the different locations
API_SHOW_URL = BASE_URL_API + "/show/{show_name}?fields=seasons&metatags=1"
API_SEASON_URL = BASE_URL_API + "/show/{show_name}/season/{season}?fields=episodes,albums&metatags=1"
API_EPISODE_URL = BASE_URL_API + "/episode/{episode_id}?fields=song-events"

# used in the head reagust to get spotify url
SPOTIFY_HEAD_LOCATION = BASE_URL + "{forward}"

# used as replacemnt for "True" for clarity
SUCCESS = True

# print templates
DASHED_TEMPALTE = " -- {} -- "
STARRED_TEMPLATE = " *** {} *** "
STAR_DASH_TEMPLATE = "  *-*-*-*- {}  *-*-*-*-  \n\n"

# validation messages printed in the scraper
NO_SUCH_SHOW_MSG = "The show you're looking for < {show_name} > doesn't exist on TUNEFIND!"
NO_SUCH_SEASON = DASHED_TEMPALTE.format("THE SHOW: {show_name} HAS NO SEASON: {season}, IS TOO {reason}")
SHOW_FULLY_SCRAPED = DASHED_TEMPALTE.format("THE SHOW: {show_name} HAS ALREADY BEEN FULLY SCRAPED!")
SEASON_FULLY_SCRAPED = DASHED_TEMPALTE.format("SHOW: {show_name}, SEASON: {season} HAS ALREADY BEEN SCRAPED!")
NO_SPOTIFY_UPDATES = "\nThere are no songs left to update for show: {show_name}, season: {season}\n"

TOTAL_REQUESTS = STARRED_TEMPLATE.format("TOTAL REQEUSTS TO BE SENT: {num_requests}")
TOTAL_SCRAPE_TIME = STARRED_TEMPLATE.format("TOTAL SCRAPING TIME BETWEEN AT LEAST: {min}s - {max}s+")
STARTING_SEASON_SCRAPE = DASHED_TEMPALTE.format("NOW STARTING TO SCRAPE EPISODES IN SEASON {season}")

SUCCESS_SCRAPE_SONGS = STAR_DASH_TEMPLATE.format("ADDED SONGS FOR {episodes} EPISODES TO THE DB")
SUCCESS_UPDATE_SPOTIFY = STAR_DASH_TEMPLATE.format("UPDATED {updates} SPOTIFY LINKS FOR SHOW: {show_name}, SEASON: {season}")

# main app print messages 
WELCOME_MSG = STARRED_TEMPLATE.format("WELCOME TO THIS AMAZING TUNEFIND SCRAPER APP")
GOODBYE_MSG = STARRED_TEMPLATE.format("THANK YOU FOR THIS TIME, PLEASE COME AGAIN!")
EVERYTHING_DELETED = STARRED_TEMPLATE.format("You just deleted EVERTYHING... No database left to work with. Now shutting down!")

DB_RESULT_MSG = "  ------  DATABASE OUTPUT FOR: {show}  ------  "

SUCCESS_MSG = DASHED_TEMPALTE.format("SUCCESS")
ERROR_MSG = DASHED_TEMPALTE.format("ERROR")
WARNING_MSG = DASHED_TEMPALTE.format("WARNING")
INVALID_NUM_MSG = DASHED_TEMPALTE.format("ERROR: Enter a vaild number!")
NOT_IMPLEMENTED_MSG = DASHED_TEMPALTE.format("I'm not going to implement this. Too many requests are going to be sent.")

DELETE_SUCCESS_MSG = "SUCCESSFULLY DELETED WHAT YOU ASKED FOR!"
DELETE_ERROR_MSG = "SOMETHING WENT WRONG DELETING THE DESIRED RESOURCE!"

# used to print different delete confirms
DELETE_TEMPLATE = "Are you sure that you want to delete {} from the database?"
CONFIRM_DELETE_EVERTHING = DELETE_TEMPLATE.format("EVERYTHING")
CONFIRM_DELETE_SHOW = DELETE_TEMPLATE.format("SHOW: {show}")
CONFIRM_DELETE_SEASON = DELETE_TEMPLATE.format("SHOW: {show} SEASON: {season}")

# used to print song counts
TOTAL_COUNT_SONGS = "THERE IS A TOTAL OF: {count} SONGS IN THE DATABASE"
TOTAL_COUNT_SHOW_SONGS = "THE SHOW: {show_name} HAS A TOTAL OF: {count} SONGS IN THE DATABASE"

# abort messages
ABORT_DELETE_MSG = "Aborted the delete operation!"
ABORT_SCRAPING_MSG = "The user does NOT wish to continue with the scraping of: < {show_name} >. Scraping aborted!"
ABORT_SPOTIFY_UPDATE_MSG = DASHED_TEMPALTE.format("THE SPOTIFY REFERER URLS ARE NO LONGER VALID!")

# all the avaialbe options to use from in the main loop
APP_OPTIONS = """SELECT AN OPTION:
        0 - EXIT
        1 - Scrape entire show
        2 - Scrape specified season
        3 - Update spotify links
        4 - Update spotify season links
        5 - List/find shows
        6 - List seasons
        7 - List episodes
        8 - List songs
        9 - Count songs
        10 - Count show songs
        11 - Delete DB show
        12 - Delete DB season
        13 - Delete EVERYTHING in DB
        14 - Export songs to csv
        15 - Export DB to script
        16 - Export DB to pickle
        17 - Export DB to JSON
        cl - Clear the screen
    """

