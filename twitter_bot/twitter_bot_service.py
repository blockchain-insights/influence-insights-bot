from tweet_templates import get_user_classification_templates
from loguru import logger
import random


class TwitterBotService:
    def __init__(self, rest_client, tweet_manager, twitter_service, file_service, test_mode=False):
        self.rest_client = rest_client
        self.tweet_manager = tweet_manager
        self.twitter_service = twitter_service
        self.file_service = file_service
        self.test_mode = test_mode

    async def fetch_and_store_tweets(self, token: str, limit_per_class: int = 1):
        """
        Fetch data for all available classifications and store random tweets for each classification.
        """
        try:
            data = await self.rest_client.fetch_account_analysis(token=token)

            # Ensure the response is structured correctly
            if not data or "results" not in data:
                logger.warning("No valid data returned from account analysis endpoint.")
                return

            classifications = {}
            for record in data["results"]:
                classification = record.get("user_classification")
                if classification:
                    classifications.setdefault(classification, []).append(record)

            for classification, users in classifications.items():
                users = random.sample(users, min(limit_per_class, len(users)))
                for user in users:
                    templates = get_user_classification_templates(user)
                    tweet_text = random.choice(templates)

                    await self.tweet_manager.add_tweet(
                        tweet_text=tweet_text,
                        user_id=user["user_id"],
                        username=user["username"],
                        classification_type=classification,
                    )

        except Exception as e:
            logger.error(f"Error fetching and storing tweets: {e}")

    async def post_random_tweet(self):
        """
        Retrieve a random tweet from a random classification and post it or save it to a file in test mode.
        """
        try:
            classifications = await self.tweet_manager.get_all_classifications()

            if not classifications:
                logger.warning("No classifications available in the database.")
                return

            random_classification = random.choice(classifications)
            random_tweet = await self.tweet_manager.get_random_tweet_by_class(random_classification)

            if not random_tweet:
                logger.warning(f"No tweets available for classification '{random_classification}'.")
                return

            if self.test_mode:
                self.file_service.append_to_file(random_tweet.tweet_text)
                logger.info(f"Tweet saved to file in test mode: {random_tweet.tweet_text}")
            else:
                response = self.twitter_service.post_tweet(random_tweet.tweet_text)
                if not response:
                    logger.error("Failed to post the tweet.")
                    return

                tweet_id = response.get("data", {}).get("id")
                logger.info(f"Successfully posted tweet with ID: {tweet_id}")
        except Exception as e:
            logger.error(f"Error posting tweet: {e}")
