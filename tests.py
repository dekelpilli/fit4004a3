import unittest
import datetime
from main import *
from unittest.mock import MagicMock
from unittest.mock import mock_open
from unittest.mock import patch

# TODO: check for branch coverage, because I can't remember what software is
# used for it

class MainTests(unittest.TestCase):
    # Tests for isInt
    def test_isInt_validBoundary(self):
        test = ArgumentHandler(None, None, None, None)
        self.assertTrue(test.isInt("-0"))
        
    def test_isInt_invalidBoundary(self):
        test = ArgumentHandler(None, None, None, None)
        self.assertFalse(test.isInt("one"))
        
    def test_isInt_regular(self):
        test = ArgumentHandler(None, None, None, None)
        self.assertTrue(test.isInt("1"))

    # Tests for checkArgumentFormats
    def test_checkArgumentFormats_noBoundaries(self):
        test = ArgumentHandler("+10:00", "2016-05-23", "2017-05-23", "@test")
        self.assertTrue(test.checkArgumentFormats())

    def test_checkArgumentFormats_allValidBoundaries(self):
        test = ArgumentHandler("-00:00", "0000-00-00", "0000-00-00", "@x")
        self.assertTrue(test.checkArgumentFormats())

    def test_checkArgumentFormats_allInvalidBoundaries(self):
        test = ArgumentHandler("+00", "00-00-0000", "00-00-0000", "@")
        self.assertFalse(test.checkArgumentFormats())

    def test_checkArgumentFormats_tZoneStrValid(self):
        test = ArgumentHandler("-00:00", "2016-05-23", "2017-05-23", "@test")
        self.assertTrue(test.checkArgumentFormats())

    def test_checkArgumentFormats_tZoneStrInvalid(self):
        test = ArgumentHandler("+00", "2016-05-23", "2017-05-23", "@test")
        self.assertFalse(test.checkArgumentFormats())

    def test_checkArgumentFormats_sDateStrValid(self):
        test = ArgumentHandler("+10:00", "0000-00-00", "2017-05-23", "@test")
        self.assertTrue(test.checkArgumentFormats())

    def test_checkArgumentFormats_sDateStrInvalid(self):
        test = ArgumentHandler("+10:00", "00-00-0000", "2017-05-23", "@test")
        self.assertFalse(test.checkArgumentFormats())

    def test_checkArgumentFormats_eDateStrValid(self):
        test = ArgumentHandler("+10:00", "2016-05-23", "0000-00-00", "@test")
        self.assertTrue(test.checkArgumentFormats())

    def test_checkArgumentFormats_eDateStrInvalid(self):
        test = ArgumentHandler("+10:00", "2016-05-23", "00-00-0000", "@test")
        self.assertFalse(test.checkArgumentFormats())

    def test_checkArgumentFormats_uHandleStrValid(self):
        test = ArgumentHandler("+10:00", "2016-05-23", "2017-05-23", "@x")
        self.assertTrue(test.checkArgumentFormats())

    def test_checkArgumentFormats_eDateStrInvalid(self):
        test = ArgumentHandler("+10:00", "2016-05-23", "2017-05-23", "@")
        self.assertFalse(test.checkArgumentFormats())

    # Tests for checkTimeZoneFormat
    def test_checkTimeZoneFormat_validBoundary(self):
        test = ArgumentHandler(None, None, None, None)
        self.assertTrue(test.checkTimeZoneFormat("-00:00"))
        
    def test_checkTimeZoneFormat_invalidBoundary(self):
        test = ArgumentHandler(None, None, None, None)
        self.assertFalse(test.checkTimeZoneFormat("+00"))
        
    def test_checkTimeZoneFormat_regular(self):
        test = ArgumentHandler(None, None, None, None)
        self.assertTrue(test.checkTimeZoneFormat("+10:00"))

    # Tests for checkDateFormat
    def test_checkDateFormat_validBoundary(self):
        test = ArgumentHandler(None, None, None, None)
        self.assertTrue(test.checkDateFormat("0000-00-00"))
        
    def test_checkDateFormat_invalidBoundary(self):
        test = ArgumentHandler(None, None, None, None)
        self.assertFalse(test.checkDateFormat("00-00-0000"))
        
    def test_checkDateFormat_regular(self):
        test = ArgumentHandler(None, None, None, None)
        self.assertTrue(test.checkDateFormat("2017-05-23"))

    # Tests for checkUserHandleFormat
    def test_checkUserHandleFormat_validBoundary(self):
        test = ArgumentHandler(None, None, None, None)
        self.assertTrue(test.checkUserHandleFormat("@x"))
        
    def test_checkUserHandleFormat_invalidBoundary(self):
        test = ArgumentHandler(None, None, None, None)
        self.assertFalse(test.checkUserHandleFormat("@"))
        
    def test_checkUserHandleFormat_regular(self):
        test = ArgumentHandler(None, None, None, None)
        self.assertTrue(test.checkUserHandleFormat("@test"))

    # Tests for formatArguments
    def test_formatArguments_noBoundaries(self):
        test = ArgumentHandler("+10:00", "2016-05-23", "2017-05-23", None)
        tZone, sDate, eDate = test.formatArguments()
        self.assertTrue(isinstance(tZone, datetime.timedelta) and isinstance(sDate, datetime.date) and isinstance(eDate, datetime.date))

    def test_formatArguments_allValidBoundaries(self):
        test = ArgumentHandler("-00:00", "0001-01-01", "0001-01-01", None)
        tZone, sDate, eDate = test.formatArguments()
        self.assertTrue(isinstance(tZone, datetime.timedelta) and isinstance(sDate, datetime.date) and isinstance(eDate, datetime.date))

    def test_formatArguments_allInvalidBoundaries(self):
        test = ArgumentHandler("+00", "01-01-0001", "01-01-0001", None)
        tZone, sDate, eDate = test.formatArguments()
        self.assertFalse(isinstance(tZone, datetime.timedelta) or isinstance(sDate, datetime.date) or isinstance(eDate, datetime.date))

    def test_formatArguments_tZoneStrValid(self):
        test = ArgumentHandler("-00:00", "2016-05-23", "2017-05-23", None)
        tZone, sDate, eDate = test.formatArguments()
        self.assertTrue(isinstance(tZone, datetime.timedelta) and isinstance(sDate, datetime.date) and isinstance(eDate, datetime.date))

    def test_formatArguments_tZoneStrInvalid(self):
        test = ArgumentHandler("+00", "2016-05-23", "2017-05-23", None)
        tZone, sDate, eDate = test.formatArguments()
        self.assertTrue((not isinstance(tZone, datetime.timedelta)) and isinstance(sDate, datetime.date) and isinstance(eDate, datetime.date))

    def test_formatArguments_sDateStrValid(self):
        test = ArgumentHandler("+10:00", "0001-01-01", "2017-05-23", None)
        tZone, sDate, eDate = test.formatArguments()
        self.assertTrue(isinstance(tZone, datetime.timedelta) and isinstance(sDate, datetime.date) and isinstance(eDate, datetime.date))

    def test_formatArguments_sDateStrInvalid(self):
        test = ArgumentHandler("+10:00", "01-01-0001", "2017-05-23", None)
        tZone, sDate, eDate = test.formatArguments()
        self.assertTrue(isinstance(tZone, datetime.timedelta) and (not isinstance(sDate, datetime.date)) and isinstance(eDate, datetime.date))

    def test_formatArguments_eDateStrValid(self):
        test = ArgumentHandler("+10:00", "2016-05-23", "0001-01-01", None)
        tZone, sDate, eDate = test.formatArguments()
        self.assertTrue(isinstance(tZone, datetime.timedelta) and isinstance(sDate, datetime.date) and isinstance(eDate, datetime.date))

    def test_formatArguments_eDateStrInvalid(self):
        test = ArgumentHandler("+10:00", "2016-05-23", "01-01-0001", None)
        tZone, sDate, eDate = test.formatArguments()
        self.assertTrue(isinstance(tZone, datetime.timedelta) and isinstance(sDate, datetime.date) and not isinstance(eDate, datetime.date))

    def test_formatArguments_tZoneValues(self):
        test = ArgumentHandler("+10:00", "2016-05-23", "2017-05-23", None)
        tZone, sDate, eDate = test.formatArguments()
        self.assertTrue(tZone.seconds == 36000)

    def test_formatArguments_sDateValues(self):
        test = ArgumentHandler("+10:00", "2016-05-23", "2017-05-23", None)
        tZone, sDate, eDate = test.formatArguments()
        self.assertTrue(sDate.year == 2016 and sDate.month == 5 and sDate.day == 23)

    def test_formatArguments_eDateValues(self):
        test = ArgumentHandler("+10:00", "2016-05-23", "2017-05-23", None)
        tZone, sDate, eDate = test.formatArguments()
        self.assertTrue(eDate.year == 2017 and sDate.month == 5 and sDate.day == 23)

    # tests for formatTimeZone
    def test_formatTimeZone_validBoundary(self):
        test = ArgumentHandler(None, None, None, None)
        self.assertIsInstance(test.formatTimeZone("-00:00"), datetime.timedelta)
        
    def test_formatTimeZone_invalidBoundary(self):
        test = ArgumentHandler(None, None, None, None)
        with self.assertRaises(IndexError):
            test.formatTimeZone("+00")
        
    def test_formatTimeZone_regular(self):
        test = ArgumentHandler(None, None, None, None)
        self.assertIsInstance(test.formatTimeZone("+10:00"), datetime.timedelta)

    def test_formatTimeZone_regularValue(self):
        test = ArgumentHandler(None, None, None, None)
        result = test.formatTimeZone("+10:00")
        self.assertEqual(result.seconds, 36000)

    def test_formatTimeZone_validBoundaryValue(self):
        test = ArgumentHandler(None, None, None, None)
        result = test.formatTimeZone("-01:01")
        self.assertEqual(result.total_seconds(), -3660)

    # tests for formatDate
    def test_formatDate_validBoundary(self):
        test = ArgumentHandler(None, None, None, None)
        self.assertIsInstance(test.formatDate("0001-01-01"), datetime.date)
        
    def test_formatDate_invalidBoundary(self):
        test = ArgumentHandler(None, None, None, None)
        self.assertEqual(test.formatDate("01-01-0001"), -1)
        
    def test_formatDate_regular(self):
        test = ArgumentHandler(None, None, None, None)
        self.assertIsInstance(test.formatDate("2017-05-24"), datetime.date)

    def test_formatDate_regularValue(self):
        test = ArgumentHandler(None, None, None, None)
        result = test.formatDate("2017-05-24")
        self.assertTrue(result.year == 2017 and result.month == 5 and result.day == 24)

    def test_formatDate_validBoundaryValue(self):
        test = ArgumentHandler(None, None, None, None)
        result = test.formatDate("0001-01-01")
        self.assertTrue(result.year == 1 and result.month == 1 and result.day == 1)

    #tests for apiCreator
    
    #because a set of keys is either valid or invalid, there is no boundary case
    
    def test_apiCreator_invalidBoundary(self):
        m = mock_open()
        with patch('__main__.open', mock_open(read_data="consumer_key= \nconsumer_secret= \naccess_token= \naccess_secret= "), create=True) as m:
            with open('codes.txt', 'r') as h:
                with self.assertRaises(tweepy.error.TweepError):
                    api = apiCreator(h)
                    
    def test_apiCreator_regular(self):
        m = mock_open()
        with patch('__main__.open', mock_open(read_data="consumer_key=yhPn4WdJK2punYXi7HgIs6Jaz\nconsumer_secret=Ess5jixcPzere2rz9yai0L55m7M59Zsukd0HiHpfZRyc4yqqiv\naccess_token=867358306662207489-PtyAQrFFxhqsp2asyarLcOqjGAPxQ3x\naccess_secret=EH3qwnLKWtZvOjOKFlZg8QO8HOeXmgHXAmXJdOkmXqPTY"), create=True) as m:
            with open('codes.txt', 'r') as h:
                api = apiCreator(h)
                h.close()

        #consumer_key is saved as a byte literal, b"a" != "a"
        self.assertTrue(api.auth.consumer_key == b"yhPn4WdJK2punYXi7HgIs6Jaz" and api.auth.consumer_secret == b"Ess5jixcPzere2rz9yai0L55m7M59Zsukd0HiHpfZRyc4yqqiv" and api.auth.access_token == "867358306662207489-PtyAQrFFxhqsp2asyarLcOqjGAPxQ3x" and api.auth.access_token_secret == "EH3qwnLKWtZvOjOKFlZg8QO8HOeXmgHXAmXJdOkmXqPTY")

    def test_apiCreator_invalidConsumerKey(self):
        m = mock_open()
        with patch('__main__.open', mock_open(read_data="consumer_key= \nconsumer_secret=Ess5jixcPzere2rz9yai0L55m7M59Zsukd0HiHpfZRyc4yqqiv\naccess_token=867358306662207489-PtyAQrFFxhqsp2asyarLcOqjGAPxQ3x\naccess_secret=EH3qwnLKWtZvOjOKFlZg8QO8HOeXmgHXAmXJdOkmXqPTY"), create=True) as m:
            with open('codes.txt', 'r') as h:
                with self.assertRaises(tweepy.error.TweepError):
                    api = apiCreator(h)

    def test_apiCreator_invalidConsumerSecret(self):
        m = mock_open()
        with patch('__main__.open', mock_open(read_data="consumer_key=yhPn4WdJK2punYXi7HgIs6Jaz\nconsumer_secret= \naccess_token=867358306662207489-PtyAQrFFxhqsp2asyarLcOqjGAPxQ3x\naccess_secret=EH3qwnLKWtZvOjOKFlZg8QO8HOeXmgHXAmXJdOkmXqPTY"), create=True) as m:
            with open('codes.txt', 'r') as h:
                with self.assertRaises(tweepy.error.TweepError):
                    api = apiCreator(h)

    def test_apiCreator_invalidAccessToken(self):
        m = mock_open()
        with patch('__main__.open', mock_open(read_data="consumer_key=yhPn4WdJK2punYXi7HgIs6Jaz\nconsumer_secret=Ess5jixcPzere2rz9yai0L55m7M59Zsukd0HiHpfZRyc4yqqiv\naccess_token= \naccess_secret=EH3qwnLKWtZvOjOKFlZg8QO8HOeXmgHXAmXJdOkmXqPTY"), create=True) as m:
            with open('codes.txt', 'r') as h:
                with self.assertRaises(tweepy.error.TweepError):
                    api = apiCreator(h)

    def test_apiCreator_invalidAccessToken(self):
        m = mock_open()
        with patch('__main__.open', mock_open(read_data="consumer_key=yhPn4WdJK2punYXi7HgIs6Jaz\nconsumer_secret=Ess5jixcPzere2rz9yai0L55m7M59Zsukd0HiHpfZRyc4yqqiv\naccess_token=867358306662207489-PtyAQrFFxhqsp2asyarLcOqjGAPxQ3x\naccess_secret= "), create=True) as m:
            with open('codes.txt', 'r') as h:
                with self.assertRaises(tweepy.error.TweepError):
                    api = apiCreator(h)

if __name__ == "__main__":
    unittest.main()
