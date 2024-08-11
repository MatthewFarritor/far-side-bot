import tweepy
import os
import random
import schedule
import time

# Twitter API credentials
bearer_token = "AAAAAAAAAAAAAAAAAAAAAKETvQEAAAAAbo09pqZXzR%2BPZVo%2BUDtp%2FGANuaY%3DeGY7nUUeAW65TMZdcRO1Y1lxIUEkQ2ab2A93YIFqFk7M9Tm9H3"
api_key = "liatL44RlGnoVCZnloOyxNcKe"
api_key_secret = "l18C1MIUQWXnlC6pbM4LtnybDWJKF8euKXVfOHpqRqjsBMuUp5"
access_token = "1821422346390925312-H4xnQFlKdJDwDxXgddFQ4Z6HguExUH"
access_token_secret = "TfSHWXxyg09NvSFRszXoc7P0spSbO5yOqdkk0G4OK9hSX"

# Authenticate to Twitter API v1.1 for media upload
auth = tweepy.OAuth1UserHandler(api_key, api_key_secret, access_token, access_token_secret)
api = tweepy.API(auth)

# Authenticate to Twitter API v2 for tweeting
client = tweepy.Client(bearer_token=bearer_token,
                       consumer_key=api_key,
                       consumer_secret=api_key_secret,
                       access_token=access_token,
                       access_token_secret=access_token_secret)

# Path to the images folder
images_folder = "images"

def tweet_random_image():
    # Get a list of all image files in the folder
    image_files = [f for f in os.listdir(images_folder) if f.endswith(('png', 'jpg', 'jpeg', 'gif'))]

    # Choose a random image
    random_image = random.choice(image_files)
    image_path = os.path.join(images_folder, random_image)

    # Tweet the random image
    try:
        # Upload the image using API v1.1
        media = api.media_upload(image_path)
        
        # Post the tweet with the image using API v2
        response = client.create_tweet(text=" ", media_ids=[media.media_id])
        
        print(f"Tweet posted successfully! Tweet ID: {response.data['id']}")
        print(f"Tweet URL: https://twitter.com/user/status/{response.data['id']}")

    except tweepy.errors.Unauthorized as e:
        print(f"Authentication failed: {e}")
    except tweepy.TweepyException as e:
        print(f"An error occurred: {e}")

# Run the tweet function immediately when the script starts
tweet_random_image()

# Schedule the tweet function to run twice a day (every 12 hours)
schedule.every(8).hours.do(tweet_random_image)

# Keep the script running to maintain the schedule
while True:
    schedule.run_pending()
    time.sleep(60)  # Check every minute for scheduled tasks
