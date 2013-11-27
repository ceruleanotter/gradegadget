'''
Created on Aug 30, 2012

@author: Lyla
'''
import re

class Section(object):
    '''
    classdocs
    '''
#I need some static class variables
#enumeration for major/minor
#method and list of major/minor
    MAJORSUBS = ["BI","CH","CS","MA","EC","GE","MA","PY","EN"]
    MAJORCOURSES = -1
    @classmethod
    def initalize(cls, coursesheet, courses_index_dic, ui):
        majorcourses = []
        for row in range(1,coursesheet.nrows):
            if (coursesheet.cell(row,courses_index_dic["School Year"]).value!=str(ui.year)):
                continue
            id = coursesheet.cell(row,courses_index_dic["ID"]).value
            if (id[0:2] in Section.MAJORSUBS and id != "CS41"):
                majorcourses.append(id)
        print "Major Courses: " 
        print majorcourses
        Section.MAJORCOURSES = majorcourses
        
    

    
    def __init__(self, sectionID, sectionName, sectionInstructor, course):
        
        #remove the s4- or s5-
        sectionName = re.sub(r"[sS][45]-", '', sectionName)
        #remove any parenthesis and anything inbetween
        sectionName = re.sub(r"\(.*\)", '', sectionName)        
        #remove any words with more then two capitol letters in a row
        sectionName = re.sub(r"[A-Z/]{2,}", '', sectionName)
        #remove Term followed by a number
        sectionName = re.sub(r"Term [0-9]{1}", '', sectionName)
        #remove S and anything with a number   
        sectionName = re.sub(r"S[0-9]{1,}", '', sectionName)
        #remove trailing spaces
        sectionName = sectionName.strip()
        
        
        
        self.id = sectionID
        self.name = sectionName
        self.teacher = sectionInstructor
        self.grade_average = -1
        self.course = course
        
        
        
    def __str__(self):
        return str(self.id) + ": " + self.name + " taught by " + self.teacher + " with average " + str(self.grade_average)