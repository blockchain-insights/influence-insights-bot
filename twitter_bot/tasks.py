from celery import shared_task
import asyncio

from settings import settings
from twitter_service import TwitterBotService
from rest_client import RestClient
from database.models.tweet import TweetManager
from database.session_manager import DatabaseSessionManager
from dotenv import load_dotenv
import os

load_dotenv()

@shared_task
def post_tweet_task():
    asyncio.run(post_tweet())

async def post_tweet():
    # Initialize REST client and database manager
    base_url = os.getenv("FETCH_API_BASE_URL", "http://localhost:9900")
    rest_client = RestClient(base_url)
    session_manager = DatabaseSessionManager()
    session_manager.init(settings.DATABASE_URL)
    tweet_manager = TweetManager(session_manager)
    twitter_bot = TwitterBotService(rest_client, tweet_manager)

    # Post tweet
    await twitter_bot.generate_and_post_tweet(token="TAO")
