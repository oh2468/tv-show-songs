from models import *
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import UnmappedInstanceError
import sqlalchemy as db
import csv
import os


class DBHandler():
    _DEFAULT_DB_NAME = "SHOW_SONGS.db"
    _DEFAULT_CSV_NAME = "SHOW_SONGS.csv"


    def __init__(self, db_name=None):
        self.db_name = db_name if db_name else self._DEFAULT_DB_NAME
        self.engine = db.create_engine(f"sqlite:///{self.db_name}")#, echo=True)
        self.engine.connect()
        init_database_tables(self.engine)


    def __insert_data(self, data):
        with Session(self.engine) as session:
            session.add(data)
            session.commit()
            session.refresh(data)
            return data


    def add_show(self, name, seasons, episodes, songs, start_date, end_date):
        db_show = Show(name=name, num_seasons=seasons, num_episodes=episodes, num_songs=songs, start_date=start_date, end_date=end_date)
        print()
        print(f"ADDING A NEW SHOW: {db_show}")
        row = self.__insert_data(db_show)
        print(row)
        print()
        return row.id


    def add_season(self, show_id, season, episodes, songs, start_date, end_date):
        db_season = Season(show_id=show_id, season=season, num_episodes=episodes, num_songs=songs, start_date=start_date, end_date=end_date)

        row = self.__insert_data(db_season)
        return row.id


    def add_episode(self, season_id, episode, name, descr, songs, air_date):
        db_episode = Episode(season_id=season_id, episode=episode, name=name, description=descr, song_count=songs, airdate=air_date)

        row = self.__insert_data(db_episode)
        return row.id


    def add_song(self, episode_id, artist, title, album, spotify_url, moment):
        db_song = Song(episode_id=episode_id, artist=artist, title=title, album=album, spotify_id=spotify_url, moment=moment)

        row = self.__insert_data(db_song)
        return row.id


    def get_song_count(self, show=None):
        with Session(self.engine) as session:
            query = session.query(Song).join(Episode).join(Season).join(Show)
            query = query.filter(Show.name == show) if show else query
            return query.count()


    def date_to_string_convert(self, columns):
        return [db.sql.func.strftime("%Y-%m-%d", column) for column in columns]


    def get_show_id(self, show_name):
        with Session(self.engine) as session:
            return session.query(Show.id).filter(Show.name == show_name).first()


    def get_season_numbers(self, show_name):
        with Session(self.engine) as session:
            return session.query(Season.season).join(Show).filter(Show.name == show_name).all() or []


    def get_shows(self, show=None):
        columns = ("Show", "Seasons", "Episodes", "Songs", "Started", "Ended")
        with Session(self.engine) as session:
            query = session.query(Show.name, Show.num_seasons, Show.num_episodes, Show.num_songs, *self.date_to_string_convert([Show.start_date, Show.end_date]))
            query = query.filter(Show.name.like(f"%{show}%")) if show else query
            return (columns, query.all())

    
    def get_seasons(self, show=None):
        columns = ("Show", "Season", "Episodes", "Songs", "Started", "Ended")
        with Session(self.engine) as session:
            query = session.query(Show.name, Season.season, Season.num_episodes, Season.num_songs, *self.date_to_string_convert([Season.start_date, Season.end_date])).select_from(Season).join(Show)
            query = query.filter(Show.name.like(f"%{show}%")) if show else query
            return (columns, query.all())


    def get_episodes(self, show=None):
        columns = ("Show", "Season", "Episode", "Song Count", "Description")
        with Session(self.engine) as session:
            query = session.query(Show.name, Season.season, Episode.episode, Episode.song_count, Episode.description).select_from(Episode).join(Season).join(Show)
            query = query.filter(Show.name.like(f"%{show}%")) if show else query
            return(columns, query.all())
            

    def get_songs(self, show=None):
        columns = ("Show", "Season", "Episode", "Artist", "Title", "Album", "Moment", "Spotify Link")
        with Session(self.engine) as session:
            query = session.query(Show.name, Season.season, Episode.episode, Song.artist, Song.title, Song.album, Song.moment, Song.spotify_id).select_from(Song).join(Episode).join(Season).join(Show)
            query = query.filter(Show.name.like(f"%{show}%")) if show else query
            return (columns, query.all())

    
    def get_spotify_forwards(self, show, season):
        with Session(self.engine) as session:
            return session.query(Song.id, Song.spotify_id).select_from(Song).join(Episode).join(Season).join(Show).filter(Show.name == show, Season.season == season).filter(Song.spotify_id.like("/forward%")).all()


    def update_spotify_link(self, song_id, spotify_url):
        with Session(self.engine) as session:
            session.query(Song).filter(Song.id == song_id).update({"spotify_id": spotify_url})
            session.commit()


    def export_songs_to_csv(self):
        columns, data = self.get_songs()
        with open(self._DEFAULT_CSV_NAME, "w", newline="", encoding="UTF-8") as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(columns)
            csv_writer.writerows(data)


    def delete_everything(self):
        with Session(self.engine) as session:
            session.query(Show).delete()
            session.commit()
        
        # if os.path.exists(self._DEFAULT_DB_NAME):
        #     os.remove(self._DEFAULT_DB_NAME)

        # if os.path.exists(self._DEFAULT_CSV_NAME):
        #     os.remove(self._DEFAULT_CSV_NAME)

    
    def delete_show(self, show):
        with Session(self.engine) as session:
            try:
                db_show = session.query(Show).filter(Show.name == show).first()
                session.delete(db_show)
                session.commit()
                return True
            except UnmappedInstanceError:
                return False


    def delete_season(self, show, season):
        with Session(self.engine) as session:
            try:    
                db_season = session.query(Season).join(Show).filter(Season.season == season, Show.name == show).first()
                session.delete(db_season)
                session.commit()
                return True
            except UnmappedInstanceError:
                return False

