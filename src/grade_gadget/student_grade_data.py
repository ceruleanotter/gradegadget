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
        self.grades = []
        print "Done creating " + self.firstName + " " + self.lastName
#        
#    def addGrade(self):
#        
#        
#    
#    class Grade(object):
#        def __init__(self, subject, mtm, etm,):
#            