from typing import Optional
import requests
from requests_oauthlib import OAuth1
from loguru import logger
from settings import Settings


class TwitterClient:
    def __init__(self, settings: Settings):
        """
        Initializes the Twitter Client using OAuth 1.0a User Context.
        """
        self.api_key = settings.TWITTER_API_KEY
        self.api_secret_key = settings.TWITTER_API_SECRET_KEY
        self.access_token = settings.TWITTER_ACCESS_TOKEN
        self.access_token_secret = settings.TWITTER_ACCESS_TOKEN_SECRET
        self.base_url = "https://api.twitter.com/2"

        # OAuth1 session
        self.auth = OAuth1(
            self.api_key,
            self.api_secret_key,
            self.access_token,
            self.access_token_secret,
        )

    def post_tweet(self, tweet_text: str) -> Optional[dict]:
        """
        Posts a tweet on behalf of the authenticated account.
        """
        url = f"{self.base_url}/tweets"
        payload = {"text": tweet_text}

        logger.debug(f"Posting tweet: {tweet_text}")

        response = requests.post(url, auth=self.auth, json=payload)

        if response.status_code == 201:  # Success
            tweet_data = response.json()
            logger.info(f"Tweet posted successfully: {tweet_data}")
            return tweet_data
        else:  # Failure
            logger.error(f"Failed to post tweet: {response.status_code} {response.text}")
            return None
