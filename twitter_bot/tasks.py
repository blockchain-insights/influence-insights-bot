from celery import shared_task
import asyncio
from settings import Settings
from twitter_bot_service import TwitterBotService
from rest_client import RestClient
from database.models.tweet import TweetManager
from database.session_manager import DatabaseSessionManager
from twitter_api.twitter_service import TwitterService
from twitter_api.twitter_client import TwitterClient
from helpers.file_service import FileService
from loguru import logger
from dotenv import load_dotenv
import os

load_dotenv()

# Task for generating and storing an insightful tweet
@shared_task
def generate_and_store_insightful_tweet_task():
    asyncio.run(generate_and_store_insightful_tweet())

async def generate_and_store_insightful_tweet():
    """
    Generates and stores an insightful tweet in the database.
    """
    try:
        base_url = os.getenv("FETCH_API_BASE_URL", "http://localhost:9900")
        rest_client = RestClient(base_url)
        settings = Settings()
        session_manager = DatabaseSessionManager()
        session_manager.init(settings.DATABASE_URL)
        tweet_manager = TweetManager(session_manager)
        twitter_bot = TwitterBotService(rest_client, tweet_manager, None, None)

        await twitter_bot.generate_and_store_tweet(token="TAO", source="fetch_insightful_data")
    except Exception as e:
        logger.error(f"Error in generate_and_store_insightful_tweet_task: {e}")

# Task for generating and storing a suspicious tweet
@shared_task
def generate_and_store_suspicious_tweet_task():
    asyncio.run(generate_and_store_suspicious_tweet())

async def generate_and_store_suspicious_tweet():
    """
    Generates and stores a suspicious tweet in the database.
    """
    try:
        base_url = os.getenv("FETCH_API_BASE_URL", "http://localhost:9900")
        rest_client = RestClient(base_url)
        settings = Settings()
        session_manager = DatabaseSessionManager()
        session_manager.init(settings.DATABASE_URL)
        tweet_manager = TweetManager(session_manager)
        twitter_bot = TwitterBotService(rest_client, tweet_manager, None, None)

        await twitter_bot.generate_and_store_tweet(token="TAO", source="fetch_suspicious_accounts")
    except Exception as e:
        logger.error(f"Error in generate_and_store_suspicious_tweet_task: {e}")

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
        test_mode = os.getenv('TEST_MODE', 'False').strip().lower() in ['true', '1', 'yes']
        twitter_bot = TwitterBotService(None, tweet_manager, twitter_service, file_service, test_mode)

        await twitter_bot.post_random_tweet()
    except Exception as e:
        logger.error(f"Error in post_random_tweet_task: {e}")
