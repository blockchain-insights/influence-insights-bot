from typing import Optional
from loguru import logger
import tweepy
from settings import Settings


class TwitterClient:
    def __init__(self, settings: Settings):
        # Initialize OAuth1.0a authentication with tokens
        self.auth = tweepy.OAuthHandler(
            settings.TWITTER_API_KEY, settings.TWITTER_API_SECRET_KEY
        )
        self.auth.set_access_token(
            settings.TWITTER_ACCESS_TOKEN, settings.TWITTER_ACCESS_TOKEN_SECRET
        )
        self.api = tweepy.API(self.auth)

    def post_tweet(self, tweet_text: str) -> Optional[dict]:
        """
        Posts a tweet on behalf of the authenticated account.
        """
        try:
            logger.debug(f"Posting tweet: {tweet_text}")
            # Use Tweepy to post the tweet
            tweet = self.api.update_status(tweet_text)
            logger.info(f"Tweet posted successfully: {tweet.id}")
            return {"id": tweet.id, "text": tweet.text}
        except tweepy.TweepyException as e:
            logger.error(f"Failed to post tweet: {e}")
            return None
