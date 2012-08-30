'''
Created on Aug 30, 2012

@author: Lyla
'''
import re
class Section(object):
    '''
    classdocs
    '''


    def __init__(self, sectionID, sectionName, sectionInstructor):
        
        #remove the s4- or s5-
        sectionName = re.sub(r"[sS][45]-", '', sectionName)
        #remove any parenthesis and anything inbetween
        sectionName = re.sub(r"\(.*\)", '', sectionName)        
        #remove any words with more then two capitol letters in a row
        sectionName = re.sub(r"[A-Z/]{2,}", '', sectionName)        
        #remove trailing spaces
        sectionName = sectionName.strip()
        
        
        
        self.id = sectionID
        self.name = sectionName
        self.teacher = sectionInstructor
        self.grade_average = -1
        
    def __str__(self):
        return str(self.id) + ": " + self.name + " taught by " + self.teacher + " with average " + str(self.grade_average)