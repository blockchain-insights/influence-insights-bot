from random import randint
from typing import Optional, List, Dict

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
    classification_type = Column(String, nullable=False)  # Updated column name
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)

class TweetManager:
    def __init__(self, session_manager):
        self.session_manager = session_manager

    async def add_tweet(self, tweet_text: str, user_id: str, username: str, classification_type: str):
        async with self.session_manager.session() as session:
            async with session.begin():
                stmt = insert(Tweet).values(
                    tweet_text=tweet_text,
                    user_id=user_id,
                    username=username,
                    classification_type=classification_type,
                    timestamp=datetime.utcnow()
                )
                await session.execute(stmt)

    async def get_random_tweet(self) -> Optional[Tweet]:
        """
        Retrieve a random tweet from the database.
        """
        async with self.session_manager.session() as session:
            total_rows_query = select(func.count()).select_from(Tweet)
            total_rows_result = await session.execute(total_rows_query)
            total_rows = total_rows_result.scalar()

            if total_rows == 0:
                return None

            random_offset = randint(0, total_rows - 1)
            random_tweet_query = select(Tweet).offset(random_offset).limit(1)
            result = await session.execute(random_tweet_query)
            return result.scalar_one_or_none()

    async def get_random_tweet_by_class(self, classification_type: str) -> Optional[Tweet]:
        """
        Retrieve a random tweet of a specific classification type from the database.
        """
        async with self.session_manager.session() as session:
            total_rows_query = (
                select(func.count())
                .select_from(Tweet)
                .where(Tweet.classification_type == classification_type)
            )
            total_rows_result = await session.execute(total_rows_query)
            total_rows = total_rows_result.scalar()

            if total_rows == 0:
                return None

            random_offset = randint(0, total_rows - 1)
            random_tweet_query = (
                select(Tweet)
                .where(Tweet.classification_type == classification_type)
                .offset(random_offset)
                .limit(1)
            )
            result = await session.execute(random_tweet_query)
            return result.scalar_one_or_none()

    async def get_all_classifications(self) -> List[str]:
        """
        Retrieve all distinct classification types from the database.
        """
        async with self.session_manager.session() as session:
            query = select(Tweet.classification_type).distinct()
            result = await session.execute(query)
            return [row[0] for row in result.fetchall()]
