import tweepy
import sys
import date



class Tweet:
    def __init__(user, text, date, time):
        self.user = user
        self.text = text
        self.date = date
        self.time = time

    def adjustTime(change):
        #TODO: adjust time of tweet by change, incl. date if it changes
        pass

def tweetAnalyser(tweets):
    #do analysis stuff
    pass

def tweetCollector(tZone, sDate, eDate, uHandle):
    #TODO: read privacy codes from file
    #TODO: read tweets from specified user, within specified dates and save as Tweet objects
    #TODO: adjust time of all tweet objects by tZone
    #return tweets

    pass
    


if __name__ == "__main__":
    print(str(sys.argv));

    #world's best error handling:
    assert '-t' in sys.argv
    assert '-a' in sys.argv
    assert '-b' in sys.argv
    assert '-i' in sys.argv
    
    timeZone = float(sys.argv[sys.argv.index('-t')+1])
    assert timeZone <= 24 and timeZone >= -24

    #TODO: do datetime stuff, less string manipulation the better
    startDate = sys.argv[sys.argv.index('-a')+1] #TODO: check that this is at least current date+tZone
    endDate = sys.argv[sys.argv.index('-b')+1]
    
    userHandle = sys.argv[sys.argv.index('-i')+1] 

    tweetCollector(timeZone, startDate, endDate, userHandle)
    print("no crash so far")
