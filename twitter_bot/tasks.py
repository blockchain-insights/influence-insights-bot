from celery import shared_task
import asyncio

from settings import settings
from twitter_bot_service import TwitterBotService
from rest_client import RestClient
from database.models.tweet import TweetManager
from database.session_manager import DatabaseSessionManager
from dotenv import load_dotenv
import os
import asyncio
from loguru import logger
from helpers.file_service import FileService
from dotenv import load_dotenv
from celery import shared_task
from rest_client import RestClient
from database.session_manager import DatabaseSessionManager
from database.models.tweet import TweetManager
from twitter_api.twitter_client import TwitterClient
from twitter_api.twitter_service import TwitterService
from twitter_bot_service import TwitterBotService
from settings import Settings

load_dotenv()

# Task for generating and storing a tweet
@shared_task
def generate_and_store_tweet_task():
    asyncio.run(generate_and_store_tweet())

async def generate_and_store_tweet():
    """
    Generates and stores a tweet in the database by analyzing insightful data.
    """
    try:
        base_url = os.getenv("FETCH_API_BASE_URL", "http://localhost:9900")
        rest_client = RestClient(base_url)
        settings = Settings()
        session_manager = DatabaseSessionManager()
        session_manager.init(settings.DATABASE_URL)
        tweet_manager = TweetManager(session_manager)
        twitter_bot = TwitterBotService(rest_client, tweet_manager, None, None)

        await twitter_bot.generate_and_store_tweet(token="TAO")
    except Exception as e:
        logger.error(f"Error in generate_and_store_tweet_task: {e}")

# Task for posting a tweet
@shared_task
def post_random_tweet_task():
    asyncio.run(post_random_tweet())

async def post_random_tweet():
    """
    Retrieves a random tweet from the database and posts it using TwitterClient.
    """
    try:
        settings = Settings()
        session_manager = DatabaseSessionManager()
        session_manager.init(settings.DATABASE_URL)
        tweet_manager = TweetManager(session_manager)
        twitter_client = TwitterClient(settings)
        twitter_service = TwitterService(twitter_client)
        file_service = FileService("test_tweets.log")
        test_mode = bool(os.getenv('TEST_MODE', False))
        twitter_bot = TwitterBotService(None, tweet_manager, twitter_service, file_service, test_mode)

        await twitter_bot.post_random_tweet()
    except Exception as e:
        logger.error(f"Error in post_random_tweet_task: {e}")
