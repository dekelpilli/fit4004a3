import unittest
import datetime
from main import *

# TODO: check for branch coverage, because I can't remember what software is
# used for it

class ArgumentHandlerTests(unittest.TestCase):
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
        with self.assertRaises(AssertionError):
            test.checkArgumentFormats()

    def test_checkArgumentFormats_tZoneStrValid(self):
        test = ArgumentHandler("-00:00", "2016-05-23", "2017-05-23", "@test")
        self.assertTrue(test.checkArgumentFormats())

    def test_checkArgumentFormats_tZoneStrInvalid(self):
        test = ArgumentHandler("+00", "2016-05-23", "2017-05-23", "@test")
        with self.assertRaises(AssertionError):
            test.checkArgumentFormats()

    def test_checkArgumentFormats_sDateStrValid(self):
        test = ArgumentHandler("+10:00", "0000-00-00", "2017-05-23", "@test")
        self.assertTrue(test.checkArgumentFormats())

    def test_checkArgumentFormats_sDateStrInvalid(self):
        test = ArgumentHandler("+10:00", "00-00-0000", "2017-05-23", "@test")
        with self.assertRaises(AssertionError):
            test.checkArgumentFormats()

    def test_checkArgumentFormats_eDateStrValid(self):
        test = ArgumentHandler("+10:00", "2016-05-23", "0000-00-00", "@test")
        self.assertTrue(test.checkArgumentFormats())

    def test_checkArgumentFormats_eDateStrInvalid(self):
        test = ArgumentHandler("+10:00", "2016-05-23", "00-00-0000", "@test")
        with self.assertRaises(AssertionError):
            test.checkArgumentFormats()

    def test_checkArgumentFormats_uHandleStrValid(self):
        test = ArgumentHandler("+10:00", "2016-05-23", "2017-05-23", "@x")
        self.assertTrue(test.checkArgumentFormats())

    def test_checkArgumentFormats_eDateStrInvalid(self):
        test = ArgumentHandler("+10:00", "2016-05-23", "2017-05-23", "@")
        with self.assertRaises(AssertionError):
            test.checkArgumentFormats()

    # Tests for checkTimeZoneFormat
    def test_checkTimeZoneFormat_validBoundary(self):
        test = ArgumentHandler(None, None, None, None)
        self.assertTrue(test.checkTimeZoneFormat("-00:00"))
        
    def test_checkTimeZoneFormat_invalidBoundary(self):
        test = ArgumentHandler(None, None, None, None)
        with self.assertRaises(AssertionError):
            test.checkTimeZoneFormat("+00")
        
    def test_checkTimeZoneFormat_regular(self):
        test = ArgumentHandler(None, None, None, None)
        self.assertTrue(test.checkTimeZoneFormat("+10:00"))

    # Tests for checkDateFormat
    def test_checkDateFormat_validBoundary(self):
        test = ArgumentHandler(None, None, None, None)
        self.assertTrue(test.checkDateFormat("0000-00-00"))
        
    def test_checkDateFormat_invalidBoundary(self):
        test = ArgumentHandler(None, None, None, None)
        with self.assertRaises(AssertionError):
            test.checkDateFormat("00-00-0000")
        
    def test_checkDateFormat_regular(self):
        test = ArgumentHandler(None, None, None, None)
        self.assertTrue(test.checkDateFormat("2017-05-23"))

    # Tests for checkUserHandleFormat
    def test_checkUserHandleFormat_validBoundary(self):
        test = ArgumentHandler(None, None, None, None)
        self.assertTrue(test.checkUserHandleFormat("@x"))
        
    def test_checkUserHandleFormat_invalidBoundary(self):
        test = ArgumentHandler(None, None, None, None)
        with self.assertRaises(AssertionError):
            test.checkUserHandleFormat("@")
        
    def test_checkUserHandleFormat_regular(self):
        test = ArgumentHandler(None, None, None, None)
        self.assertTrue(test.checkUserHandleFormat("@test"))

    # Tests for formatArguments TODO

if __name__ == "__main__":
    unittest.main()
