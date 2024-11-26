import random
from loguru import logger
from database.models.tweet import TweetManager
from rest_client import RestClient
from twitter_api.twitter_service import TwitterService
from helpers.file_service import FileService  # Import the FileService


class TwitterBotService:
    def __init__(
        self,
        rest_client: RestClient,
        tweet_manager: TweetManager,
        twitter_service: TwitterService,
        file_service: FileService,
        test_mode: bool = False,  # Add test mode flag
    ):
        self.rest_client = rest_client
        self.tweet_manager = tweet_manager
        self.twitter_service = twitter_service
        self.file_service = file_service
        self.test_mode = test_mode  # Initialize the flag

    async def generate_and_store_tweet(self, token: str):
        """
        Fetches data from an API, generates a tweet, and stores it in the database.
        """
        try:
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

            # Templates for tweet generation
            templates = [
                # Template 1: High-level overview of anomaly
                (
                    f"🚨 Suspicious activity detected: {selected_user['anomaly_type']} 🚨\n"
                    f"@{selected_user['username']} | Followers: {selected_user['follower_count']} | Verified: {'✅' if selected_user.get('is_verified') else '❌'}\n"
                    f"Engagement: {selected_user['avg_engagement']:.2f} | Tweets: {selected_user['tweet_count']}\n"
                    f"Highlight: \"{selected_user['recent_tweets'][0]}\"\n"
                    f"🔗 {selected_user['tweet_urls'][0]}\n\n"
                    f"🌐 Explore more anomalies on $COMAI Subnet!"
                ),
                # Template 2: Specific anomaly focus
                (
                    f"🧐 Anomaly alert: {selected_user['anomaly_type']}!\n"
                    f"User @{selected_user['username']} has {'unusually high' if selected_user['anomaly_type'] == 'High Engagement Low Followers' else 'unusually low'} engagement.\n"
                    f"Followers: {selected_user['follower_count']}, Engagement Level: {selected_user['avg_engagement']:.2f}\n"
                    f"Recent Activity: \"{selected_user['recent_tweets'][0]}\"\n"
                    f"Details here: {selected_user['tweet_urls'][0]} 🌍\n\n"
                    f"🌟 Stay informed with Influence Insights on $COMAI!"
                ),
                # Template 3: Regional anomaly focus
                (
                    f"🌍 Regional anomaly detected: {selected_user['anomaly_type']} from {selected_user.get('region_name', 'an unknown region')}.\n"
                    f"User @{selected_user['username']} posted: \"{selected_user['recent_tweets'][0]}\"\n"
                    f"Metrics: Followers - {selected_user['follower_count']}, Engagement - {selected_user['avg_engagement']:.2f}\n"
                    f"🔗 {selected_user['tweet_urls'][0]}\n\n"
                    f"Uncover regional trends on $COMAI Subnet!"
                ),
                # Template 4: Engagement and behavior anomaly
                (
                    f"🚨 Behavioral anomaly: {selected_user['anomaly_type']} 🚨\n"
                    f"User: @{selected_user['username']} | Followers: {selected_user['follower_count']}\n"
                    f"Engagement: {selected_user['avg_engagement']:.2f} | Total Likes: {selected_user['total_likes']}\n"
                    f"\"{selected_user['recent_tweets'][0]}\"\n"
                    f"🔗 Find more: {selected_user['tweet_urls'][0]} 🌟\n\n"
                    f"🌐 Powered by Influence Insights on $COMAI!"
                ),
                # Template 5: Call to action
                (
                    f"🚨 Unusual activity: {selected_user['anomaly_type']}!\n"
                    f"@{selected_user['username']} | Followers: {selected_user['follower_count']} | Likes: {selected_user['total_likes']}\n"
                    f"Tweet Highlight: \"{selected_user['recent_tweets'][0]}\"\n"
                    f"See the anomaly here: {selected_user['tweet_urls'][0]}\n\n"
                    f"🌐 Actionable insights with Influence Insights on $COMAI!"
                ),
                # Template 6: Focused on suspicious behavior
                (
                    f"⚠️ Suspicious metrics detected for @{selected_user['username']}:\n"
                    f"Followers: {selected_user['follower_count']} | Engagement: {selected_user['avg_engagement']:.2f}\n"
                    f"Activity: \"{selected_user['recent_tweets'][0]}\"\n"
                    f"Check this out: {selected_user['tweet_urls'][0]}\n\n"
                    f"Stay informed on $COMAI Subnet!"
                ),
                # Template 7: Highlighting anomaly with a question
                (
                    f"🤔 What's going on with @{selected_user['username']}?\n"
                    f"Anomaly: {selected_user['anomaly_type']}.\n"
                    f"Metrics: Followers - {selected_user['follower_count']}, Engagement - {selected_user['avg_engagement']:.2f}\n"
                    f"\"{selected_user['recent_tweets'][0]}\"\n"
                    f"🔗 {selected_user['tweet_urls'][0]}\n\n"
                    f"🌟 Influence Insights powered by $COMAI!"
                ),
            ]

            # Generate tweet using a random template
            tweet_text = random.choice(templates)

            logger.info(f"Generated Tweet: {tweet_text}")

            # Save the tweet to the database
            await self.tweet_manager.add_tweet(
                tweet_text=tweet_text,
                user_id=selected_user["user_id"],
                username=selected_user["username"],
                anomaly_type=selected_user["anomaly_type"]
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
