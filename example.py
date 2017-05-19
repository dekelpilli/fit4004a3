import tweepy

if __name__ == "__main__":
    # We need consumer_key and consumer_secret from a valid Twitter application
    auth = tweepy.OAuthHandler("YTfdTejS0WWcAPSmw4fiQ8xPX", "hl0XsCaljgZrjIgCtoWsEq6RG4NDFCOKv66ixHUnKMqqhBOmE4")
    auth.set_access_token("95835448-loErRxTXlyomzGgZj0lmJ1HBoEvmWdXFONVfe1JNM", "21G2KPjE8baTIjU7r5pNKSbW2FR6KJvNfogeilxrShTch")

    api = tweepy.API(auth)

    public_tweets = api.home_timeline()
    badCountProgramming101 = 0
    for tweet in public_tweets:
        badCountProgramming101 += 1
        print(tweet.text + " (" + str(badCountProgramming101) + ")\n--------------------------\n\n")
