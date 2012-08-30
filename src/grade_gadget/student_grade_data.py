'''
Created on Aug 30, 2012

@author: Lyla
'''

class Student(object):
    '''
    classdocs
    '''


    def __init__(self, firstName, lastName, username, combo="undecided", advisor="none"):
        self.firstName = firstName
        self.lastName = lastName
        self.combo = combo
        self.advisor = advisor
        self.username=username
        print "Done creating " + self.firstName + " " + self.lastName
        