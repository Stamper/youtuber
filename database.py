from yaml import load, BaseLoader
from datetime import datetime

from sqlalchemy import create_engine, Column, Date, DateTime, Integer, BigInteger, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

SETTINGS = 'settings.yaml'
with open(SETTINGS, 'r') as stream:
    config = load(stream, Loader=BaseLoader)

engine = create_engine(config['database'], encoding='utf-8')
Base = declarative_base()


class Video(Base):
    __tablename__ = 'videos'

    video_id = Column(String(11), primary_key=True, index=True)
    channel = Column(String(50))
    title = Column(String(200))
    published_at = Column(Date)


class Views(Base):
    __tablename__ = 'views'

    id = Column(Integer, primary_key=True)
    video_id = Column(String(11), ForeignKey('videos.video_id'), index=True)
    timestamp = Column(DateTime, index=True)
    count = Column(BigInteger)
    likes = Column(BigInteger)
    dislikes = Column(BigInteger)

    def __init__(self, video_id, count, likes, dislikes):
        self.video_id = video_id
        self.count = count
        self.likes = likes
        self.dislikes = dislikes
        self.timestamp = datetime.now()


if __name__ == '__main__':
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
