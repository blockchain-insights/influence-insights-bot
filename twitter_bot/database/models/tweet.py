from random import randint
from typing import Optional

from sqlalchemy import Column, Integer, String, DateTime, select, func
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

    async def get_random_tweet(self) -> Optional[Tweet]:
        """
        Retrieves a random tweet from the database.
        """
        async with self.session_manager.session() as session:
            # Get total number of rows
            total_rows_query = select(func.count()).select_from(Tweet)
            total_rows_result = await session.execute(total_rows_query)
            total_rows = total_rows_result.scalar()

            if total_rows == 0:
                return None

            # Generate a random offset
            random_offset = randint(0, total_rows - 1)

            # Fetch the tweet at the random offset
            random_tweet_query = select(Tweet).offset(random_offset).limit(1)
            result = await session.execute(random_tweet_query)
            random_tweet = result.scalar_one_or_none()

            return random_tweet
