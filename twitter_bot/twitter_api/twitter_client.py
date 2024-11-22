from typing import Optional

from loguru import logger
import requests
from ratelimit import limits, sleep_and_retry
from settings import Settings


class TwitterClient:
    def __init__(self, settings: Settings):
        self.bearer_token = settings.TWITTER_BEARER_TOKEN

    def create_headers(self):
        return {"Authorization": f"Bearer {self.bearer_token}"}

    @sleep_and_retry
    @limits(calls=15, period=15 * 60)  # Twitter rate limit: 15 calls per 15 minutes
    def post_tweet(self, tweet_text: str) -> Optional[dict]:
        url = "https://api.twitter.com/2/tweets"
        headers = self.create_headers()
        payload = {"text": tweet_text}

        logger.debug(f"Posting tweet: {tweet_text}")
        response = requests.post(url, headers=headers, json=payload)

        if response.status_code != 201:  # Status code 201 for successful creation
            logger.error(f"post_tweet: Request error {response.status_code} {response.text}")
            return None

        return response.json()
