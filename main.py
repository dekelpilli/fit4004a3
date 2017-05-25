import tweepy
import sys
import datetime
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt


class Tweet:
    #user is a string, @rgmerk
    #text is a string containing content of tweet
    #date is a datetime.date() object
    #time is a datetime.time() object
    def __init__(self, user, date, time):
        self.user = user
        self.date = date
        self.time = time

    #delta is a timedelta object
    def adjustTime(self, delta):
        date = datetime.datetime.combine(self.date, self.time)
        date += delta
        self.time = date.time()
        self.date = date.date()



#tweets contains Tweet objects, sDate and eDate are datetime.date() objects
def plotTweets(tweets, sDate, eDate):
    times = {}
    for i in range(24):
        times[i] = 0 #fill out hashmap keys

    for tweet in tweets:
        times[tweet.time.hour] += 1

    days = (eDate - sDate).days + 1
    
    frequency = []
    for time in times:
        frequency.append(times[time]/days)
    #print(frequency)
    plt.plot(frequency)
    plt.ylabel("Average tweets per day")
    plt.xlabel("Time of day")
    fig = plt.gcf()
    return fig


def getCode(line):
    return line.split("=")[1].strip()


#codeFile is an already opened file
def createApi(codeFile):
    codes = codeFile.readlines()
    codeFile.close()

    for line in codes:
        if line.count("consumer_key=") == 1:
            consumerKey = getCode(line)
        elif line.count("consumer_secret=") == 1:
            consumerSecret = getCode(line)
        elif line.count("access_token=") == 1:
            accessToken = getCode(line)
        elif line.count("access_secret=") == 1:
            accessSecret = getCode(line)

    #set up API
    auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
    auth.set_access_token(accessToken, accessSecret)
    api = tweepy.API(auth)

    api.verify_credentials()

    return api



# tZone is timedelta
# sDate and eDate are datetime objects
# uHandle is string, starting with @
def collectTweets(tZone, sDate, eDate, uHandle, api):

    collectedTweets = [] #stores Tweet objects
    pageNum = 1

    tweetIds = {}

    #read tweets from specified user, within specified dates and save as Tweet objects
    while True:
        tweets = api.user_timeline(uHandle, page = pageNum) #tweets contains 20 tweets. Every time pageNum increases, it moves on to the next 20.
        
        #if there are no more tweets and sDate hasn't been reached yet
        if len(tweets) == 0:
            return collectedTweets
        for tweet in tweets:
            if tweet.id in tweetIds:
                return collectedTweets #returns to visited tweet, finish to avoid infinite loops. Good failsafe, but should, theoretically, only get user while testing.
            else:
                tweetIds[tweet.id] = True
            
            tweetTime = tweet.created_at #datetime object of when tweet was created
            tweetObj = Tweet(uHandle, tweetTime.date(), tweetTime.time()) #converts collected tweet into a Tweet object. also possible to get username from tweet using api.get_user(tweet.user.id).screen_name
            tweetObj.adjustTime(tZone)
            tweetTime = tweetObj.date
            
            if tweetTime >= sDate and tweetTime <= eDate: #if date is valid, add tweet to list
                collectedTweets.append(tweetObj)

            
            elif tweetTime < sDate: #if tweet is before valid range, exit (because we're reading from newest to oldest)
                return collectedTweets #return tweets
        pageNum += 1


    return collectedTweets

# TODO: move this into another file because it's bloody huge
class ArgumentHandler:
    def __init__(self, tZone, sDate, eDate, uHandle):
        self.tZoneStr = tZone
        self.sDateStr = sDate
        self.eDateStr = eDate
        self.uHandleStr = uHandle

    # helper function that checks if string corresponds to an int
    def isInt(self, string):
        try:
            int(string)
            return True
        except ValueError:
            return False

    # checks that all args are in correct format
    def checkArgumentFormats(self):
        validTz = self.checkTimeZoneFormat(self.tZoneStr)

        validDates = True
        dates = [self.sDateStr, self.eDateStr]
        for date in dates:
            validDates = validDates and self.checkDateFormat(date)

        validUser = self.checkUserHandleFormat(self.uHandleStr)
        return validTz and validDates and validUser

    #the following three methods check that the command line arguments given are in the correct format
    def checkTimeZoneFormat(self, tZone):
        try:
            assert len(tZone) == 6
            assert tZone[0] in ["+", "-"]
            assert tZone[3] == ":"
            assert self.isInt(tZone[1]) and self.isInt(tZone[2]) and self.isInt(tZone[4]) and self.isInt(tZone[5])
        except AssertionError:
            return False
        return True

    def checkDateFormat(self, date):
        try:
            assert len(date) == 10
            assert date[4] == "-" and date[7] == "-"
            assert self.isInt(date[0]) and self.isInt(date[1]) and self.isInt(date[2]) and self.isInt(date[3]) and self.isInt(date[5]) and self.isInt(date[6]) and self.isInt(date[8]) and self.isInt(date[9])
        except AssertionError:
            return False
        return True

    def checkUserHandleFormat(self, uHandle):
        try:
            assert len(uHandle) > 1
            assert uHandle[0] == "@"
        except AssertionError:
            return False
        return True

    # the following 3 mehtods take strings from command line args and formats them into more useful objects
    # assumes that strings are in correct format
    def formatArguments(self):
        # turn timezone string into timedelta obj
        tZone = None
        try:
            tZone = self.formatTimeZone(self.tZoneStr)
        except IndexError:
            tZone = -1

        #turn start and end date strings into date obj
        sDate = self.formatDate(self.sDateStr)
        eDate = self.formatDate(self.eDateStr)

        return tZone, sDate, eDate

    def formatTimeZone(self, tZoneStr):
        sign = tZoneStr[0]
        time = tZoneStr[1:]
        time = time.split(":")
        tHours = int(time[0])
        tMinutes = int(time[1])
        if sign == "-":
            tHours = 0-tHours
            tMinutes = 0-tMinutes
        return datetime.timedelta(hours=tHours, minutes=tMinutes)

    def formatDate(self, dateStr):
        date = dateStr.split("-")
        if len(date[0]) < 4:
            return -1
        year = int(date[0])
        month = int(date[1])
        day = int(date[2])
        return datetime.date(year, month, day)

def validateArgumentObjectValues(timeZone, startDate, endDate):
    try:
        # between -23:55hrs and 23:55hrs
        assert timeZone.seconds >= -86100 and timeZone.seconds <= 86100
        assert startDate <= endDate
        return True
    except AssertionError:
        return False

if __name__ == "__main__":
    print(str(sys.argv));


    assert '-a' in sys.argv
    assert '-b' in sys.argv
    assert '-i' in sys.argv

    if '-t' in sys.argv:
        timeZoneBase = sys.argv[sys.argv.index('-t')+1]
    else:
        timeZoneBase = "+00:00"

    startDateBase = sys.argv[sys.argv.index('-a')+1] 
    endDateBase = sys.argv[sys.argv.index('-b')+1]
    userHandle = sys.argv[sys.argv.index('-i')+1]

    argHandler = ArgumentHandler(timeZoneBase, startDateBase, endDateBase, userHandle)
    
    if not argHandler.checkArgumentFormats():
        raise ValueError

    # format args into better objs
    timeZone, startDate, endDate = argHandler.formatArguments()
    if not validateArgumentObjectValues(timeZone, startDate, endDate):
        raise ValueError

    # generate API
    api = createApi(open("codes.txt", "r"))

    tweets = collectTweets(timeZone, startDate, endDate, userHandle, api)
    
    tweetMessage = "Frequency of tweets by " + userHandle + " between " + startDateBase + " and " + endDateBase + ". Timezone: UTC" + timeZoneBase #message to be tweeted out with image

    plot = plotTweets(tweets, startDate, endDate) #save plot reference
    plot.savefig("plot.png", bbox_inches="tight") #save file
    
    api.update_with_media("plot.png", status=tweetMessage) #tweet it out to the world, available on https://twitter.com/A3Fit4004
