import random
from loguru import logger
from database.models.tweet import TweetManager
from rest_client import RestClient


class TwitterBotService:
    def __init__(self, rest_client: RestClient, tweet_manager: TweetManager):
        self.rest_client = rest_client
        self.tweet_manager = tweet_manager

    async def generate_and_post_tweet(self, token: str):
        try:
            # Fetch data from the REST API
            data = await self.rest_client.fetch_insightful_data(token=token)

            # Debug: Log raw response
            logger.debug(f"Raw response from API: {data}")

            # Validate and extract data
            if isinstance(data, dict) and "response" in data:
                data = data["response"]
            else:
                logger.error("Unexpected data format: 'response' key missing.")
                return

            if not isinstance(data, list):
                logger.error("Unexpected data format: 'response' is not a list.")
                return

            # Filter anomalies
            anomalies = [item for item in data if isinstance(item, dict) and item.get("anomaly_type") != "Normal"]
            if not anomalies:
                logger.warning("No anomalies found.")
                return

            # Select a random user with an anomaly
            selected_user = random.choice(anomalies)

            # Generate tweet content
            tweet_text = (
                f"🚨 Anomaly detected: {selected_user['anomaly_type']} 🚨\n"
                f"User: @{selected_user['username']} | Followers: {selected_user['follower_count']}\n"
                f"Engagement: {selected_user['avg_engagement']:.2f} | Tweets: {selected_user['tweet_count']}\n"
                f"Recent: {selected_user['recent_tweets'][0]}\n"
                f"🔗 {selected_user['tweet_urls'][0]}"
            )

            # Log the tweet
            logger.info(f"Generated Tweet: {tweet_text}")

            # Save to the database
            await self.tweet_manager.add_tweet(
                tweet_text=tweet_text,
                user_id=selected_user["user_id"],
                username=selected_user["username"],
                anomaly_type=selected_user["anomaly_type"]
            )

        except Exception as e:
            logger.error(f"Error generating tweet: {e}")