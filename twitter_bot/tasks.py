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

# Task for generating and storing tweets by classification
@shared_task
def generate_and_store_tweets_task():
    asyncio.run(generate_and_store_tweets())

async def generate_and_store_tweets():
    """
    Fetch data for all classifications and store tweets in the database.
    """
    try:
        # Initialize required components
        base_url = os.getenv("FETCH_API_BASE_URL", "http://localhost:9900")
        rest_client = RestClient(base_url)
        settings = Settings()
        session_manager = DatabaseSessionManager()
        session_manager.init(settings.DATABASE_URL)
        tweet_manager = TweetManager(session_manager)
        twitter_client = TwitterClient(settings)
        twitter_service = TwitterService(twitter_client)

        # Create TwitterBotService instance
        twitter_bot = TwitterBotService(
            rest_client=rest_client,
            tweet_manager=tweet_manager,
            twitter_service=None,  # Not used here
            file_service=None,  # Not used here
            test_mode=False
        )

        # Fetch and store tweets for all classifications
        await twitter_bot.fetch_and_store_tweets(token="TAO")
    except Exception as e:
        logger.error(f"Error in generate_and_store_tweets_task: {e}")

# Task for posting a random tweet
@shared_task
def post_random_tweet_task():
    asyncio.run(post_random_tweet())

async def post_random_tweet():
    """
    Retrieve a random tweet from the database and post it using TwitterClient.
    """
    try:
        # Initialize required components
        settings = Settings()
        session_manager = DatabaseSessionManager()
        session_manager.init(settings.DATABASE_URL)
        tweet_manager = TweetManager(session_manager)
        twitter_client = TwitterClient(settings)
        twitter_service = TwitterService(twitter_client)
        file_service = FileService("test_tweets.log")

        # Check if the bot is in test mode
        test_mode = os.getenv('TEST_MODE', 'False').strip().lower() in ['true', '1', 'yes']

        # Create TwitterBotService instance
        twitter_bot = TwitterBotService(
            rest_client=None,  # Not used here
            tweet_manager=tweet_manager,
            twitter_service=twitter_service,
            file_service=file_service,
            test_mode=test_mode
        )

        # Post a random tweet
        await twitter_bot.post_random_tweet()
    except Exception as e:
        logger.error(f"Error in post_random_tweet_task: {e}")
