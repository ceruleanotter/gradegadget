'''
Created on Aug 30, 2012

@author: Lyla
'''

class Student(object):
    '''
    classdocs
    '''


    def __init__(self, name, sclass, advisor, combo, classes, comments):
        self.name = name
        self.sclass = sclass
        self.advisor = advisor
        self.combo = combo
        self.classes = classes
        self.comments = comments
        print "Done creating " + self.name
        
    
    def __str__(self):
        return self.name + ", Combo: " + self.combo