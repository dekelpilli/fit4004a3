import tweepy
import sys
import datetime



class Tweet:
    def __init__(self, user, text, date, time):
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
        self.checkTimeZoneFormat(self.tZoneStr) 
        
        dates = [self.sDateStr, self.eDateStr]
        for date in dates:
            self.checkDateFormat(date)
        
        self.checkUserHandleFormat(self.uHandleStr)
        return True

    def checkTimeZoneFormat(self, tZone):
        assert len(tZone) == 6
        assert tZone[0] in ["+", "-"]
        assert tZone[3] == ":"
        assert self.isInt(tZone[1]) and self.isInt(tZone[2]) and self.isInt(tZone[4]) and self.isInt(tZone[5])
        return True

    def checkDateFormat(self, date):
        assert len(date) == 10
        assert date[4] == "-" and date[7] == "-"
        assert self.isInt(date[0]) and self.isInt(date[1]) and self.isInt(date[2]) and self.isInt(date[3]) and self.isInt(date[5]) and self.isInt(date[6]) and self.isInt(date[8]) and self.isInt(date[9])
        return True

    def checkUserHandleFormat(self, uHandle):
        assert len(uHandle) > 1
        assert uHandle[0] == "@"
        return True

    # takes strings from command line args and formats them into more useful objects
    # assumes that strings are in correct format
    def formatArguments(self):
        # turn timezone string into timedelta obj
        tZone = formatTimeZone(self.tZoneStr)

        #turn start and end date strings into date obj
        sDate = formatDate(self.sDateStr)
        eDate = formatDate(self.eDateStr)

        return tZone, sDate, eDate

    def formatTimeZone(self, tZoneStr):
        sign = tZoneStr[0]
        time = tZoneStr[1:]
        time = tZoneStr.split(":")
        tHours = int(time[0])
        tMinutes = int(time[1])
        if sign == "-":
            tHours = 0-tHours
            tMinutes = 0-tMinutes
        return timedate.timedelta(hours=tHours, minutes=tMinutes)

    def formatDate(self, dateStr):
        date = dateStr.split("-")
        year = int(date[0])
        month = int(date[1])
        day = int(date[2])
        return timedate.date(year, month, day)

if __name__ == "__main__":
    print(str(sys.argv));

    #world's best error handling:
    assert '-t' in sys.argv
    assert '-a' in sys.argv
    assert '-b' in sys.argv
    assert '-i' in sys.argv

    timeZoneBase = sys.argv[sys.argv.index('-t')+1]
    startDateBase = sys.argv[sys.argv.index('-a')+1] #TODO: check that this is less than current date+tZone
    endDateBase = sys.argv[sys.argv.index('-b')+1]
    userHandle = sys.argv[sys.argv.index('-i')+1]

    # I don't think this is correct. The spec says use ':', not '.'
    
    #timeZone = float(sys.argv[sys.argv.index('-t')+1])
    #assert timeZone <= 24 and timeZone >= -24

    argHandler = ArgumentHandler(timeZoneBase, startDateBase, endDateBase, userHandleBase)
    # assert format of command line args
    try:
        argHandler.checkArgumentFormats()
    except AssertionError:
        # TODO: add messages to each assertion
        sys.exit("At least one argument was in the incorrect format")

    # format args into better objs
        timeZone, startDate, endDate = argHandler.formatArguments()

    tweetCollector(timeZone, startDate, endDate, userHandle)
    print("no crash so far")
