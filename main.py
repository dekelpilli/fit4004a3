import tweepy
import sys
import datetime
import requests
#from datetime import tzinfo
import matplotlib.pyplot as plt


class Tweet:
    #user is a string, @rgmerk
    #text is a string containing content of tweet
    #date is a datetime.date() object
    #time is a datetime.time() object

    #def __init__(self, user, text, date, time):
    def __init__(self, user, date, time):
        self.user = user
        #self.text = text
        self.date = date
        self.time = time

    #change is a timedelta object
    def adjustTime(self, delta):
        date = datetime.datetime.combine(self.date, self.time)
        date += delta
        self.time = date.time()
        self.date = date.date()

##def uploadPlot(api, plotName):
##    api.update_with_media(plotName)


#Tweet objects
def plotTweets(tweets, sDate, eDate):
    times = {}
    for i in range(24):
        times[i] = 0

    for tweet in tweets:
        times[tweet.time.hour] += 1

    #days = (min(eDate, datetime.datetime.now().date()) - sDate).days + 1 #if we don't want to include days beyond today in the average
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
    #fig.savefig("plot.png", bbox_inches="tight")

def getCode(line):
    return line.split("=")[1].strip()

def createApi(codeFile):
    #read privacy codes from file
    codes = codeFile.readlines()
    codeFile.close()

    #print(codes)

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
        #print("XX LOGGING: tweets = " + str(tweets))

        #if there are no more tweets and sDate hasn't been reached yet
        if len(tweets) == 0:
            #print(str(len(collectedTweets)) + " tweets makes me angry")
            return collectedTweets
        for tweet in tweets:
            if tweet.id in tweetIds:
                return collectedTweets #returns to visited tweet, finish to avoid infinite loops. Good failsafe, but should, theoretically, only get user while testing.
            else:
                tweetIds[tweet.id] = True
            
            tweetTime = tweet.created_at
            #tweetObj = Tweet(uHandle, tweet.text.encode('UTF-8'), tweetTime.date(), tweetTime.time()) #text not needed, only for testing
            tweetObj = Tweet(uHandle, tweetTime.date(), tweetTime.time()) #converts collected tweet into a Tweet object. also possible to get username from tweet using api.get_user(tweet.user.id).screen_name
            tweetObj.adjustTime(tZone)
            tweetTime = tweetObj.date
            
            if tweetTime >= sDate and tweetTime <= eDate:
                collectedTweets.append(tweetObj)

            elif tweetTime < sDate:
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

    # takes strings from command line args and formats them into more useful objects
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

    #world's best error handling:
    #assert '-t' in sys.argv
    assert '-a' in sys.argv
    assert '-b' in sys.argv
    assert '-i' in sys.argv

    if '-t' in sys.argv:
        timeZoneBase = sys.argv[sys.argv.index('-t')+1]
    else:
        timeZoneBase = "00:00"

    startDateBase = sys.argv[sys.argv.index('-a')+1] #TODO: check that this is less than current date+tZone
    endDateBase = sys.argv[sys.argv.index('-b')+1]
    userHandle = sys.argv[sys.argv.index('-i')+1]

    # I don't think this is correct. The spec says use ':', not '.'

    #timeZone = float(sys.argv[sys.argv.index('-t')+1])
    #assert timeZone <= 24 and timeZone >= -24

    argHandler = ArgumentHandler(timeZoneBase, startDateBase, endDateBase, userHandle)
    # assert format of command line args
##    try:
##        argHandler.checkArgumentFormats()
##    except AssertionError:
##        # TODO: add messages to each assertion
##        sys.exit("At least one argument was in the incorrect format")
    
    if not argHandler.checkArgumentFormats():
        raise ValueError

    # format args into better objs
    timeZone, startDate, endDate = argHandler.formatArguments()
    if not validateArgumentObjectValues(timeZone, startDate, endDate):
        raise ValueError

    # generate API
    api = createApi(open("codes.txt", "r"))

    tweets = collectTweets(timeZone, startDate, endDate, userHandle, api)
    
    #print(len(tweets))
##    for tweet in tweets:
##        print(tweet.text)
    plot = plotTweets(tweets, startDate, endDate)

    tweetMessage = "Frequency of tweets by " + userHandle + " between " + startDateBase + " and " + endDateBase + ". Timezone: UTC" + timeZoneBase
    
    api.update_with_media("plot.png", status=tweetMessage)
