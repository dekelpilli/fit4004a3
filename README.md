# FlowUnderStacks - Assignment 3

## Getting started  
To run this program, you need to have Tweepy and Python 3.5.2 installed. If you do not, follow the instructions [here](https://github.com/tweepy/tweepy/blob/master/README.md) and [here](https://wiki.python.org/moin/BeginnersGuide/Download) to do so.

To start the program, open the terminal in the folder that contains main.py and enter the following command:

### For Linux:
python main.py -t [timezone] -a [startDate] -b [endDate] -i [userId]

### For Windows:
main.py -t [timezone] -a [startDate] -b [endDate] -i [userId]

#### timezone
Formatted as +/-HH:MM. This is the amount of time to add to any given tweet's time when recorded in the user's time zone.   
*Example:* -05:30

#### startDate & endDate 
Formatted as YYYY-MM-DD. When to start and end the tweet analysis.   
*Example:* 2017-05-20

#### userId
Formatted as @userIdHere. The handle of the user whose tweets you want analysed.  
*Example:* @rgmerk

## Test Selection Strategy
The selection of test cases will involve multiple selection strategies. These strategies will be defined in a specific order of execution when generating test cases, with the intention of earlier strategies being more specific and generating tests for the most common and useful functionality, and later ones being useful for generating tests for edge cases that the previous strategies may miss.

### Strategies 

#### Black box strategies 
Our black box testing will include these strategies, in the following order: 
##### Boundary Value analysis on unit inputs 
For each input for the tested unit, two boundary values and one non-boundary value will be tested. Based on the purpose/specifications of the unit, this will include one valid boundary value, one invalid, and one non-boundary value.  
  
For example, an input that corresponds to the user&rsquo;s age could have the values 0, -1, and 30.  
   
If a unit being tested has more than one input, the following tests should be conducted:  
* No boundary values  
* All valid boundary values  
* All invalid boundary values  
* A test for each input&rsquo;s boundary values in isolation (i.e. no other inputs have boundary values at the same time)  

Hence, for a unit with two inputs, there should be 7 tests run (the first three dot points, then 2 for each input: one for valid boundary and one for invalid).

##### Exploratory testing 
Once tests have been developed via the boundary value analysis, the team will check for requirement coverage and try to come up with tests for any requirements that aren&rsquo;t covered. 

#### White box strategies 
Our white box testing will include these strategies, in the following order: 
##### Branch coverage testing 
Once black box tests have been developed, a branch coverage check will be run. New tests will need to be developed for any branches that have not been covered by the black box tests. 

##### Statement coverage
After branch coverage has been done, we will check for statement (or LOC) coverage. As with branch coverage testing, we will develop the tests necessary to cover any statements without tests.

##### Exploratory testing
Once all other white box testing methods have been exhausted, we will add tests to any remaining features or aspects of the program that we feel aren’t sufficiently tested. 

### Rationale
Due to the simple nature of our system, and the fact that we’ll be using both black box and white box testing techniques, we&rsquo;ve decided that our black box tests should be mostly to test for the absence of features/functionality. With that in mind, we adopted boundary value analysis to check that the requirements are being met.  
<br/>
Our white box testing techniques are being used primarily to ensure that our black box techniques have not completely missed entire sections of code by accident. Due to the simple nature of the system, 100% coverage is being required by our tests, given that that should not result in too large a test suite.  
<br/>
Exploratory testing will be used to supplement the above techniques and cover anything we&rsquo;ve missed. We expect that exploratory white box testing will produce very few tests.
