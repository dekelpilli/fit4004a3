import tweepy
import sys
import datetime
from datetime import tzinfo


class Tweet:
    #user is a string, @rgmerk
    #text is a string containing content of tweet
    #date is a datetime.date() object
    #time is a datetime.time() object
    def __init__(self, user, text, date, time):
        self.user = user
        self.text = text
        self.date = date
        self.time = time

    #change is a timedelta object
    def adjustTime(self, delta):
        date = datetime.datetime.combine(self.date, self.time)
        date += delta
        self.time = date.time()
        self.date = date.date()

def tweetAnalyser(tweets):
    #do analysis stuff
    pass


def getCode(line):
    return line.split("=")[1].strip()

def apiCreator(codeFile):
    #read privacy codes from file
    #codes = open(filename, "r").readlines()
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



## params are as given by user
def tweetCollector(tZone, sDate, eDate, uHandle, codeFile):
    api = apiCreator(codeFile)

    collectedTweets = [] #stores Tweet objects
    pageNum = 0

    #read tweets from specified user, within specified dates and save as Tweet objects
    while True:
        tweets = api.user_timeline(uHandle, page = pageNum) #tweets contains 20 tweets. Every time pageNum increases, it moves on to the next 20.

        #if there are no more tweets and
        if len(tweets) == 0:
            return collectedTweets
        for tweet in tweets:
            tweetTime = tweet.created_at
            tweetObj = Tweet(uHandle, tweet.text, tweetTime.date(), tweetTime.time()) #converts collected tweet into a Tweet object. also possible to get username from tweet using api.get_user(tweet.user.id).screen_name
            tweetObj.adjustTime(tZone)
            tweetTime = datetime.datetime.combine(tweetObj.date(), tweetObj.time())
            
            if tweetTime >= sDate and tweetTime <= eDate:
                collectedTweets.append(tweetObj)




            elif tweetTime < sDate:
                continue
            elif tweetTime > eDate:
                #TODO: adjust time of all tweet objects by tZone

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
        try:
            sDate = self.formatDate(self.sDateStr)
        except IndexError:
            sDate = -1

        try:
            eDate = self.formatDate(self.eDateStr)
        except IndexError:
            eDate = -1

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

    tweetCollector(timeZone, startDate, endDate, userHandle,open("codes.txt", "r"))
    print("no crash so far")
