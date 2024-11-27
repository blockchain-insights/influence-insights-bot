from tweet_templates import get_insightful_templates, get_suspicious_templates
from loguru import logger
import random


class TwitterBotService:
    def __init__(self, rest_client, tweet_manager, twitter_service, file_service, test_mode=False):
        self.rest_client = rest_client
        self.tweet_manager = tweet_manager
        self.twitter_service = twitter_service
        self.file_service = file_service
        self.test_mode = test_mode

    async def fetch_data(self, token: str, source: str) -> list:
        """
        Fetch data from the configured endpoint.
        :param token: Token to filter data.
        :param source: Source of data ("fetch_insightful_data" or "fetch_suspicious_accounts").
        :return: List of data items.
        """
        try:
            if source == "fetch_insightful_data":
                data = await self.rest_client.fetch_insightful_data(token=token)
            elif source == "fetch_suspicious_accounts":
                data = await self.rest_client.fetch_suspicious_accounts(token=token)
            else:
                raise ValueError(f"Unknown data source: {source}")

            # Validate and return data
            if isinstance(data, dict) and "response" in data:
                return data["response"]
            else:
                logger.error(f"Unexpected data format from {source} endpoint.")
                return []

        except Exception as e:
            logger.error(f"Error fetching data from source '{source}': {e}")
            return []

    async def generate_and_store_tweet(self, token: str, source: str = "fetch_insightful_data"):
        """
        Generate and store a tweet from either insightful or suspicious data.
        """
        try:
            data = await self.fetch_data(token=token, source=source)

            if not data:
                logger.warning("No data available for tweet generation.")
                return

            # Filter anomalies
            anomalies = [item for item in data if item.get("suspicious_types") or item.get("anomaly_type")]
            if not anomalies:
                logger.warning("No anomalies found.")
                return

            # Select a random user
            selected_user = random.choice(anomalies)

            # Fetch appropriate templates
            templates = (
                get_insightful_templates(selected_user)
                if source == "fetch_insightful_data"
                else get_suspicious_templates(selected_user)
            )

            # Generate tweet
            tweet_text = random.choice(templates)

            logger.info(f"Generated Tweet: {tweet_text}")

            # Save tweet
            await self.tweet_manager.add_tweet(
                tweet_text=tweet_text,
                user_id=selected_user["user_id"],
                username=selected_user["username"],
                anomaly_type=", ".join(selected_user.get("suspicious_types", [])),
            )
        except Exception as e:
            logger.error(f"Error generating tweet: {e}")

    async def post_random_tweet(self):
        """
        Retrieve a random tweet from the database and post it or save it to a file in test mode.
        """
        try:
            random_tweet = await self.tweet_manager.get_random_tweet()

            if not random_tweet:
                logger.warning("No tweets available to post.")
                return

            if self.test_mode:
                # Append tweet to file in test mode
                self.file_service.append_to_file(random_tweet.tweet_text)
                logger.info("Tweet appended to file in test mode.")
            else:
                # Post the tweet using the TwitterClient
                response = self.twitter_service.post_tweet(random_tweet.tweet_text)

                if not response:
                    logger.error("Failed to post the tweet.")
                    return

                tweet_id = response.get("data", {}).get("id")
                logger.info(f"Successfully posted tweet with ID: {tweet_id}")
        except Exception as e:
            logger.error(f"Error posting random tweet: {e}")