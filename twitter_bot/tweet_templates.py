# tweet_templates.py

def get_insightful_templates(selected_user):
    return [
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
            f"🌍 Regional anomaly detected: {selected_user['anomaly_type']} from {selected_user.get('region_name') or 'an unknown region'}.\n"
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


def get_suspicious_templates(selected_user):
    # Determine singular/plural for anomalies
    anomalies = selected_user.get("suspicious_types", [])
    anomaly_text = (
        f"an anomaly: {anomalies[0]}" if len(anomalies) == 1 else f"multiple anomalies: {', '.join(anomalies)}"
    )

    return [
        # Template 1: General anomaly detection
        (
            f"⚠️ Suspicious Activity Detected ⚠️\n"
            f"User @{selected_user['username']} triggered {anomaly_text}.\n"
            f"Followers: {selected_user['follower_count']}, Engagement: {selected_user['avg_engagement']:.2f}\n"
            f"Recent Activity: \"{selected_user['recent_tweets'][0]}\"\n"
            f"🔗 Check more anomalies: {selected_user['tweet_urls'][0]}\n\n"
            f"🌟 Explore detailed insights on $COMAI Subnet!"
        ),
        # Template 2: Regional focus
        (
            f"🚨 Regional Alert 🚨\n"
            f"User @{selected_user['username']} detected with {anomaly_text} in "
            f"{selected_user.get('region_name', 'Unknown Region')}.\n"
            f"Followers: {selected_user['follower_count']} | Engagement: {selected_user['avg_engagement']:.2f}\n"
            f"Tweet: \"{selected_user['recent_tweets'][0]}\"\n"
            f"🔗 Explore anomalies: {selected_user['tweet_urls'][0]}\n\n"
            f"🌐 Stay ahead with Influence Insights powered by $COMAI!"
        ),
        # Template 3: Engagement and anomaly focus
        (
            f"🚨 Behavioral Alert 🚨\n"
            f"@{selected_user['username']} shows {anomaly_text}.\n"
            f"Followers: {selected_user['follower_count']} | Engagement: {selected_user['avg_engagement']:.2f}\n"
            f"Recent Highlight: \"{selected_user['recent_tweets'][0]}\"\n"
            f"🔗 Investigate further: {selected_user['tweet_urls'][0]}\n\n"
            f"🌟 Powered by Influence Insights on $COMAI Subnet!"
        ),
        # Template 4: Highlighting unusual activity
        (
            f"🤔 What's happening with @{selected_user['username']}?\n"
            f"Detected {anomaly_text}.\n"
            f"Metrics: Followers - {selected_user['follower_count']}, Engagement - {selected_user['avg_engagement']:.2f}\n"
            f"\"{selected_user['recent_tweets'][0]}\"\n"
            f"🔗 Learn more: {selected_user['tweet_urls'][0]}\n\n"
            f"🌐 Insights by $COMAI Subnet!"
        ),
        # Template 5: Call-to-action for anomalies
        (
            f"⚠️ Unusual Metrics Detected ⚠️\n"
            f"@{selected_user['username']} with {anomaly_text}.\n"
            f"Followers: {selected_user['follower_count']} | Tweets: {selected_user['tweet_count']} | Likes: {selected_user['total_likes']}\n"
            f"Activity Highlight: \"{selected_user['recent_tweets'][0]}\"\n"
            f"🔗 Explore details: {selected_user['tweet_urls'][0]}\n\n"
            f"🌟 Stay informed with $COMAI Influence Insights!"
        ),
        # Template 6: Regional anomaly with behavioral highlight
        (
            f"🌍 Anomaly in Focus 🌍\n"
            f"User @{selected_user['username']} detected with {anomaly_text}.\n"
            f"Region: {selected_user.get('region_name', 'Unknown')} | Engagement: {selected_user['avg_engagement']:.2f}\n"
            f"\"{selected_user['recent_tweets'][0]}\"\n"
            f"🔗 Check the full story: {selected_user['tweet_urls'][0]}\n\n"
            f"Powered by $COMAI Subnet!"
        ),
        # Template 7: Engagement vs anomaly metrics
        (
            f"📊 Suspicious Metrics 📊\n"
            f"@{selected_user['username']} detected with {anomaly_text}.\n"
            f"Metrics: Followers - {selected_user['follower_count']}, Engagement - {selected_user['avg_engagement']:.2f}, Likes - {selected_user['total_likes']}\n"
            f"Activity: \"{selected_user['recent_tweets'][0]}\"\n"
            f"🔗 Learn more: {selected_user['tweet_urls'][0]}\n\n"
            f"🌟 Influence Insights on $COMAI Subnet!"
        ),
    ]

