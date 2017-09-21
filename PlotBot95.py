# Dependencies
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import json
import tweepy
import time
import seaborn as sns

# Initialize Sentiment Analyzer
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
analyzer = SentimentIntensityAnalyzer()

# Twitter API Keys
consumer_key = "cMnVNrJEbsCv3easQWejUmbOQ"
consumer_secret = "EjpNKfimw2QvhgvtNCaZsASrQggLQtCerXJaSHjVdFV7yCf2c1"
access_token = "887647238574440449-VyVoau5lTmu0enGGxIc8j8265NtQwv8"
access_token_secret = "QjOonCIFm2F0F4kK6pmJZtJn36qf4M7qGTGvzMDxQu7sT"

# Create a global variable to pass through both functions
target_list = []
target_user = ''

# Function is made to find mentions of my twitter handle
def find_me():
    print('starting find me fxn')

    # Setup Tweepy API Authentication
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())
    
    # Target Term
    target_term = "@jeffrey_coen"
    
    # Search for all tweets
    public_tweets = api.search(target_term, count=1, result_type="recent")

   # Loop through all public_tweets
    for tweet in public_tweets["statuses"]:

        # Get ID and Author of most recent tweet directed to me
        tweet_id = tweet["id"]
        tweet_author = tweet["user"]["screen_name"]
        tweet_text = tweet["text"]
        
        # Split the tweet 
        targeted_user = tweet_text.split()

        # Print the user to analyze
        target_user = targeted_user[-1]

    # Return values to be used in the next fxn
    return target_user, tweet_author

# Create a function to perform the requested sentiment analysis
def perform_sentiment():
    print("starting sentiment fxn")

     # Setup Tweepy API Authentication
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

    # Target Account
    target_user = find_me()[0]
    tweet_author = find_me()[1]

    # Spam filter.  If target user does not appear in the list, then we perform analysis in the else startment
    if target_user in target_list:
            print(target_user + " has already had analysis performed")

    else:
        # Append list of analyzed names
        target_list.append(target_user)

        # Counter
        counter = 0

        # Variables for holding sentiments
        sentiments = []

        # Loop through 5 pages of tweets (total 100 tweets)
        for x in range(25):

            # Get all tweets from home feed
            public_tweets = api.user_timeline(target_user, page = x)

            # Loop through all tweets 
            for tweet in public_tweets:

                # Run Vader Analysis on each tweet
                compound = analyzer.polarity_scores(tweet["text"])["compound"]
                
                # Add sentiments for each tweet into an array
                sentiments.append({"Date": tweet["created_at"], "Compound": compound,})
                
                # Add to counter 
                counter = counter + 1
            
        # Convert sentiments to DataFrame
        sentiments_pd = pd.DataFrame.from_dict(sentiments)
        sentiments_pd.head()

        print("There were " + str(counter) + ' tweets analyzed for sentiment')

        # Create plot
        plt.plot(np.arange(len(sentiments_pd["Compound"])), sentiments_pd["Compound"], marker="o", linewidth=0.5, alpha=0.8)

        # # Incorporate the other graph properties
        plt.title("Sentiment Analysis of Tweets (%s) for %s" % (time.strftime("%x"), target_user))
        plt.ylabel("Tweet Polarity")
        plt.xlabel("Tweets Ago")

        # Save the figure
        plt.savefig("PlotBot.png")
        
        # Create a status update
        api.update_with_media("PlotBot.png", "Sentiment analysis of " + target_user + ".  Thanks " + tweet_author + "!!")
        print('Thanks ' + tweet_author + '!!')
        
while(True):
    find_me()
    perform_sentiment()
    time.sleep(300)