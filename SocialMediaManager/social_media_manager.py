import tweepy
from instabot import Bot

class SocialMediaManager:
    def __init__(self, twitter_api_key, twitter_api_secret, twitter_access_token, twitter_access_secret,
                 instagram_username, instagram_password):
        auth = tweepy.OAuth1UserHandler(
            twitter_api_key, twitter_api_secret,
            twitter_access_token, twitter_access_secret
        )
        self.api = tweepy.API(auth)
        logger.info("Twitter API authenticated successfully.")

        self.instagram_bot = Bot()
        self.instagram_bot.login(username=instagram_username, password=instagram_password)
        logger.info("Instagram API authenticated successfully.")

    def create_tweet(self, blog_title: str, blog_url: str) -> str:
        """
        Creates a tweet based on the blog title and URL.
        """
        try:
            tweet = f"📢 New Blog Post: {blog_title}\nRead more: {blog_url} #Balooger #Blogging"
            logger.debug(f"Generated tweet: {tweet}")
            return tweet
        except Exception as e:
            logger.error(f"Error creating tweet: {e}")
            return ""

    def post_tweet(self, tweet: str) -> None:
        """
        Posts the tweet to Twitter.
        """
        try:
            self.api.update_status(tweet)
            logger.info("Tweet posted successfully.")
        except Exception as e:
            logger.error(f"Error posting tweet: {e}")

    def create_instagram_caption(self, blog_title: str, summary: str) -> str:
        """
        Creates an Instagram caption based on the blog title and summary.
        """
        try:
            caption = f"✨ New Blog Alert! ✨\n\n{blog_title}\n\n{summary}\n\n#Balooger #Blogging #Python #Tech"
            logger.debug(f"Generated Instagram caption: {caption}")
            return caption
        except Exception as e:
            logger.error(f"Error creating Instagram caption: {e}")
            return ""

    def post_instagram(self, image_path: str, caption: str) -> None:
        """
        Posts the image with the caption to Instagram.
        """
        try:
            self.instagram_bot.upload_photo(image_path, caption=caption)
            logger.info("Instagram post created successfully.")
        except Exception as e:
            logger.error(f"Error posting to Instagram: {e}")