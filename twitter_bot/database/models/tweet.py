from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.dialects.postgresql import insert
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from database import OrmBase

Base = declarative_base()

class Tweet(OrmBase):
    __tablename__ = 'tweets'
    id = Column(Integer, primary_key=True, autoincrement=True)
    tweet_text = Column(String, nullable=False)
    user_id = Column(String, nullable=False)
    username = Column(String, nullable=False)
    anomaly_type = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)


class TweetManager:
    def __init__(self, session_manager):
        self.session_manager = session_manager

    async def add_tweet(self, tweet_text: str, user_id: str, username: str, anomaly_type: str):
        async with self.session_manager.session() as session:
            async with session.begin():
                stmt = insert(Tweet).values(
                    tweet_text=tweet_text,
                    user_id=user_id,
                    username=username,
                    anomaly_type=anomaly_type,
                    timestamp=datetime.utcnow()
                )
                await session.execute(stmt)
