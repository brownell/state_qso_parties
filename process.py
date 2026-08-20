
from read_prepare import read_prepare
from cross_check import cross_check

def prepare():

    '''
        Read in all the log files, save the Cabrillo object and the data, 
        save values that will be needed later
    '''
    read_prepare()

    '''
    Do the cross-checking, marking qsos that fail the match test.
    Warning messages are generated when qso fails match
    Failed qsos marked invalid so not counted in score
    '''
    cross_check()