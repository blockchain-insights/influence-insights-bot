from loguru import logger
from typing import Optional
from twitter_api.twitter_client import TwitterClient


class TwitterService:
    def __init__(self, twitter_client: TwitterClient):
        self.twitter_client = twitter_client

    def post_tweet(self, tweet_text: str) -> Optional[dict]:
        """
        Posts a tweet and returns the tweet ID if successful.
        """
        try:
            response = self.twitter_client.post_tweet(tweet_text)
            if not response:
                logger.error("Failed to post tweet.")
                return None

            logger.info(f"Successfully posted tweet: {response}")
            return response  # Return the tweet ID if available
        except Exception as e:
            logger.error(f"Error posting tweet: {e}")
            return None
