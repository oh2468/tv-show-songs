from enum import unique
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Text, UniqueConstraint
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Show(Base):
    __tablename__ = "show"

    id = Column(Integer, primary_key=True)
    name = Column(String(64, collation="NOCASE"), nullable=False, unique=True)
    num_seasons = Column(Integer)
    num_episodes = Column(Integer)
    num_songs = Column(Integer)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    #seasons = relationship("Season", cascade="all, delete, delete-orphan")
    seasons = relationship("Season", backref="from_show")

    def __repr__(self):
        return f"{self.name}, {self.num_seasons}, {self.num_episodes}, {self.num_songs}, {self.start_date}, {self.end_date}"


class Season(Base):
    __tablename__ = "season"

    id = Column(Integer, primary_key=True)
    show_id = Column(Integer, ForeignKey("show.id", ondelete="CASCADE"))
    season = Column(Integer, nullable=False)
    num_episodes = Column(Integer, nullable=False)
    num_songs = Column(Integer, nullable=False)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    #episodes = relationship("Episode", cascade="all, delete, delete-orphan")
    episodes = relationship("Episode", backref="from_season")
    
    __table_args__ =  (UniqueConstraint("show_id", "season", name="unique_season"), )

    def __repr__(self):
        return f"{self.show_id}, {self.season}, {self.num_episodes}, {self.num_songs}, {self.start_date}, {self.end_date}"


class Episode(Base):
    __tablename__ = "episode"

    id = Column(Integer, primary_key=True)
    season_id = Column(Integer, ForeignKey("season.id", ondelete="CASCADE"))
    episode = Column(Integer, nullable=False)
    name = Column(String(64), nullable=False)
    description = Column(Text)
    song_count = Column(Integer, nullable=False)
    airdate = Column(DateTime)
    #songs = relationship("Song", cascade="all, delete, delete-orphan")
    songs = relationship("Song", backref="from_episode")
    
    __table_args__ =  (UniqueConstraint("season_id", "episode", name="unique_episode"), )

    def __repr__(self):
        return f"{self.season_id}, {self.episode}, {self.name}, {self.description}, {self.song_count}, {self.airdate}"


class Song(Base):
    __tablename__ = "song"

    id = Column(Integer, primary_key=True)
    episode_id = Column(Integer, ForeignKey("episode.id", ondelete="CASCADE"))
    artist = Column(String(64), nullable=False)
    title = Column(String(64), nullable=False)
    album = Column(String(64), nullable=False)
    spotify_id = Column(String(128))
    moment = Column(Text)

    def __repr__(self):
        return f"{self.episode_id}, {self.artist}, {self.title}, {self.album}, {self.moment}, {self.spotify_id}"



def init_database_tables(engine):
    Base.metadata.create_all(engine)

