import requests
import random
import time
from base64 import b64encode
from settings import *
from database_handler import DBHandler
from datetime import datetime


class TunefindScraper():

    def __init__(self, show_name):
        self.show_name = show_name.strip().lower().replace(" ", "-")
        self.readable_show_name = show_name.strip().lower()
        self.session = requests.Session()
        self.init_session()
        self.dbHandler = DBHandler()


    def init_session(self):
        print(f"SESSION INITIALIZED FOR SHOW: {self.show_name}")
        print(BASE_URL_SHOW.format(show_name=self.show_name))
        self.session.headers.update({"User-Agent": MY_USER_AGENT})
        resp = self.session.get(BASE_URL_SHOW.format(show_name=self.show_name))
        if resp.status_code != 200:
            raise ValueError(NO_SUCH_SHOW_MSG.format(show_name=self.show_name))


    def user_wants_to_exit(self):
        raise SystemExit(ABORT_SCRAPING_MSG.format(show_name=self.readable_show_name)) 

    
    def get_request_to_json(self, url):
        print(f"REQUEST SENT TO: {url}")
        return self.session.get(url).json()
    

    def head_location_from_request(self, url):
        return self.session.head(url).headers["location"]


    def get_user_confirmation(self):
        while(answer := input("Are you sure that you want to continue? (y/n): ")) != "y":
            if answer == "n":
                self.user_wants_to_exit()


    def confirm_num_requests_to_send(self, num_requests):
        min = round(num_requests * SCRAPE_DELAY_MIN, 2)
        max = round(num_requests * SCRAPE_DELAY_MAX, 2)

        print(TOTAL_REQUESTS.format(num_requests=num_requests))
        print(TOTAL_SCRAPE_TIME.format(min=min, max=max))

        self.get_user_confirmation()


    def request_delayer(self):
        time.sleep(random.uniform(SCRAPE_DELAY_MIN, SCRAPE_DELAY_MAX))


    def extract_show_info(self, base):
        show_name = base["show"]["name"]
        seasons = base["seasons"]
        num_seasons = len(seasons)
        num_episodes, num_songs = 0, 0

        for season in seasons:
            num_episodes += season["episodes_count"]
            num_songs += season["songs_count"]
        
        start_date = seasons[0]["air_date_start"]
        end_date = seasons[-1]["air_date_end"]
        st = datetime.fromtimestamp(start_date)
        en = datetime.fromtimestamp(end_date)

        #print(f"SHOW: {show_name}, SEASONS: {seasons}, EPISODES: {enum_episodesps}, SONGS: {num_songs}, RUN: {s_start} - {s_end}")
        #self.get_user_confirmation(num_seasons + num_episodes)

        show_id = self.dbHandler.add_show(show_name, num_seasons, num_episodes, num_songs, st, en)
        return show_id


    def extract_season_info(self, db_show_id, season):
        s_id = season["group_sequence"]
        eps = season["episodes_count"]
        songs = season["songs_count"]
        start = season["air_date_start"]
        end = season["air_date_end"]
        s_start = datetime.fromtimestamp(start)
        s_end = datetime.fromtimestamp(end)

        #print(f"SHOW: {db_show_id}, SEASONS: {s_id}, EPISODES: {eps}, SONGS: {songs}, RUN: {s_start} - {s_end}")

        db_season_id = self.dbHandler.add_season(db_show_id, s_id, eps, songs, s_start, s_end)
        return (db_season_id, s_id)


    def extract_episode_info(self, db_season_id, episode):
        tune_ep_id = episode["id"]
        name = episode["name"]
        e_id = episode["number"]
        descr = episode["description"]
        songs = episode["songs_count"]
        air_date = episode["air_date"]
        s_air_date = datetime.fromtimestamp(air_date)

        #print(f"SEASON: {db_season_id}, EPISODE: {e_id}, NAME: {name}, SONGS: {songs}, AIRED: {s_air_date}, DESCRIPTION: {descr}")
        try:
            db_episode_id = self.dbHandler.add_episode(db_season_id, e_id, name, descr, songs, s_air_date)
            return (db_episode_id, tune_ep_id)
        except:
            return (None, None)


    def extract_song_info(self, db_episode_id, episode_details, show, season, tune_id):
        referer = f"https://www.tunefind.com/show/{show}/season-{season}/{tune_id}"
        ref_b64_enc = b64encode(referer.encode("UTF-8")).decode("UTF-8")
        for event in episode_details["episode"]["song_events"]: 
            song = event["song"]
            artist = song["artists"][0]["name"]
            title = song["name"]
            album = song["album"]
            moment = event["description"]
            if (spotify_id := song['spotify']):
                spotify_id = spotify_id.replace("referer=", f"referer={ref_b64_enc}")

            #print(f"ARTIST: {artist}, TITLE: {title}, ALBUM: {album}, SPOTIFY: {spotify_id}, MOMEMENT: {moment}")

            self.dbHandler.add_song(db_episode_id, artist, title, album, spotify_id, moment)


    def count_episodes(self, seasons):
        return sum(season["episodes_count"] for season in seasons)


    def show_fully_scraped(self, show):
        return self.count_episodes(show["seasons"]) == len(self.dbHandler.get_episodes(self.show_name)[1])


    def scrape_show(self, season=None):
        if season and season < 1:
            return (not SUCCESS, NO_SUCH_SEASON.format(show_name=self.readable_show_name, season=season, reason="LOW"))
            
        show = self.get_request_to_json(API_SHOW_URL.format(show_name=self.show_name))

        if season and len(show["seasons"]) < season:
            return (not SUCCESS, NO_SUCH_SEASON.format(show_name=self.readable_show_name, season=season, reason="HIGH"))

        if self.show_fully_scraped(show):
            return (not SUCCESS, SHOW_FULLY_SCRAPED.format(show_name=self.readable_show_name))

        seasons_to_scrape = [show["seasons"][season - 1]] if season else show["seasons"]
        num_requests = self.count_episodes(seasons_to_scrape)

        self.confirm_num_requests_to_send(num_requests)

        scraped_seasons = [sid[0] for sid in self.dbHandler.get_season_numbers(self.readable_show_name)]

        if season and season in scraped_seasons:
            return (not SUCCESS, SEASON_FULLY_SCRAPED.format(show_name=self.readable_show_name, season=season))
        elif (show_id := self.dbHandler.get_show_id(self.readable_show_name)):
            db_show_id = show_id[0]
        else:
            db_show_id = self.extract_show_info(show)

        num_requests_made = 0

        for seasn in seasons_to_scrape:
            if seasn["group_sequence"] in scraped_seasons:
                continue

            db_season_id, s_num = self.extract_season_info(db_show_id, seasn)
            episodes = self.get_request_to_json(API_SEASON_URL.format(show_name=self.show_name, season=s_num))

            print(STARTING_SEASON_SCRAPE.format(season=s_num))
            for episode in episodes["episodes"]:
                db_episode_id, tune_ep_id = self.extract_episode_info(db_season_id, episode)
                
                if episode["songs_count"] > 0 and tune_ep_id:
                    ## going to SLEEP, trying not to send too many requests in a row ##
                    self.request_delayer()

                    ep_details = self.get_request_to_json(API_EPISODE_URL.format(show_name=self.show_name, episode_id=tune_ep_id))
                    self.extract_song_info(db_episode_id, ep_details, self.show_name, s_num, tune_ep_id)

                    num_requests_made += 1

        return (SUCCESS, SUCCESS_SCRAPE_SONGS.format(episodes=num_requests_made))


    def update_spotify_links(self, season):
        songs_to_update = self.dbHandler.get_spotify_forwards(self.readable_show_name, season)

        if not songs_to_update:
            return (not SUCCESS, NO_SPOTIFY_UPDATES.format(show_name=self.readable_show_name, season=season))
        else:
            self.confirm_num_requests_to_send(len(songs_to_update))

        for song in songs_to_update:
            ## going to SLEEP, trying not to send too many requests in a row ##
            self.request_delayer()
            
            song_id, forwrd = song
            
            spotify_url = self.head_location_from_request(SPOTIFY_HEAD_LOCATION.format(forward=forwrd))
            print(spotify_url)

            if "tunefind" in spotify_url:
                print(ERROR_MSG)
                raise SystemExit(ABORT_SPOTIFY_UPDATE_MSG)

            self.dbHandler.update_spotify_link(song_id, spotify_url)

        return (SUCCESS, SUCCESS_UPDATE_SPOTIFY.format(updates=len(songs_to_update), show_name=self.readable_show_name, season=season))


