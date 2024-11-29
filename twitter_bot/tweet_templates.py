def get_user_classification_templates(selected_user):
    """
    Generate diverse templates for user classifications based on unified endpoint data.
    """
    user_classification = selected_user.get("user_classification", "Unknown Classification")
    username = selected_user.get("username", "Unknown User")
    followers = selected_user.get("follower_count", 0)
    engagement = selected_user.get("avg_engagement", 0.0)
    tweets = selected_user.get("tweet_count", 0)
    total_likes = selected_user.get("total_likes", 0)
    max_likes = selected_user.get("max_likes", 0)
    region = selected_user.get("region_name", "Unknown Region")
    recent_tweet = selected_user.get("recent_tweets", ["No recent tweet"])[0]
    tweet_url = selected_user.get("tweet_urls", ["No URL"])[0]

    return [
        # Template 1: High-level overview
        (
            f"📊 Classification: {user_classification}\n"
            f"User: @{username} | Followers: {followers}\n"
            f"Engagement: {engagement:.2f} | Tweets: {tweets} | Max Likes: {max_likes}\n"
            f"Recent Tweet: \"{recent_tweet}\"\n"
            f"🔗 Check it out: {tweet_url}\n\n"
            f"Stay updated with $COMAI insights!"
        ),
        # Template 2: Highlight regional focus
        (
            f"🌍 Regional Insight: {user_classification} in {region}\n"
            f"User @{username} | Followers: {followers}, Engagement: {engagement:.2f}\n"
            f"Highlight: \"{recent_tweet}\"\n"
            f"🔗 More details: {tweet_url}\n\n"
            f"Discover regional trends with $COMAI Subnet!"
        ),
        # Template 3: Behavior spotlight
        (
            f"🚨 Behavioral Classification: {user_classification} 🚨\n"
            f"User @{username} | Followers: {followers}\n"
            f"Engagement: {engagement:.2f} | Total Likes: {total_likes}\n"
            f"Recent Activity: \"{recent_tweet}\"\n"
            f"🔗 Learn more: {tweet_url}\n\n"
            f"Insights powered by $COMAI!"
        ),
        # Template 4: Metrics breakdown
        (
            f"📈 Metrics Breakdown:\n"
            f"User @{username} | Classification: {user_classification}\n"
            f"Followers: {followers} | Engagement: {engagement:.2f} | Tweets: {tweets}\n"
            f"Highlight: \"{recent_tweet}\"\n"
            f"🔗 Check the full story: {tweet_url}\n\n"
            f"Powered by Influence Insights on $COMAI!"
        ),
        # Template 5: Engagement focus
        (
            f"🔥 Engagement Spotlight 🔥\n"
            f"@{username} classified as {user_classification}.\n"
            f"Followers: {followers} | Engagement: {engagement:.2f}\n"
            f"Top Activity: \"{recent_tweet}\"\n"
            f"🔗 Explore more: {tweet_url}\n\n"
            f"Stay ahead with $COMAI Subnet!"
        ),
        # Template 6: Call to action
        (
            f"🧐 Curious about @{username}'s activity?\n"
            f"Classification: {user_classification}\n"
            f"Followers: {followers}, Engagement: {engagement:.2f}\n"
            f"Recent Tweet: \"{recent_tweet}\"\n"
            f"🔗 Dive deeper: {tweet_url}\n\n"
            f"Actionable insights powered by $COMAI!"
        ),
        # Template 7: Anomaly-based classification
        (
            f"🚨 User @{username} flagged as {user_classification}.\n"
            f"Metrics: Followers - {followers}, Engagement - {engagement:.2f}, Tweets - {tweets}\n"
            f"Recent Activity: \"{recent_tweet}\"\n"
            f"🔗 Investigate: {tweet_url}\n\n"
            f"Stay informed with $COMAI Subnet!"
        ),
    ]
