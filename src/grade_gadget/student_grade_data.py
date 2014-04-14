'''
Created on Aug 30, 2012

@author: Lyla
'''
from course_section import Section
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
        self.gpa = -1
        self.currentYear = ""
        
    def addGrade(self,subject, mtm, etm, final, comment):        
        self.grades.append(self.Grade(subject.name, mtm, etm, final, subject.grade_average,
                                       subject.teacher, comment, subject.course))

        
    def calculateGPA(self, isFinal):

        sum = 0;
        dividedBy =0;
        if Section.MAJORCOURSES == -1:
            raise Exception("MAJORCOURSES in course_section was not initalize, please do this before calculating GPAs")
        for grade in self.grades:
            try:
                if isFinal:
                    numGrade = float(grade.etm)
                else:
                    numGrade = float(grade.mtm)
            except ValueError:
                #print "No grade for " + grade.subject
                continue
            if (grade.course in Section.MAJORCOURSES):
                sum += (2*numGrade)
                dividedBy +=2
            else:
                sum += numGrade
                dividedBy+=1
        if dividedBy != 0:
            self.gpa = round(sum/dividedBy,2)
        else:
            print "gpa calculation failed for " + self.firstName + " " + self.lastName
    
    
    def __str__(self):
        gradesoutput = ""
        for g in self.grades:
            gradesoutput += str(g)
            gradesoutput += "\n"
        return self.firstName + " " + self.lastName + ", Combo: " + self.combo + " Grades: " + gradesoutput
    
    class Grade(object):
        def __init__(self, subject, mtm, etm,final,ave,teacher,comment,course):
            self.subject = subject
            self.mtm = mtm
            self.etm = etm
            self.final = final
            self.average = ave
            self.comment = comment
            self.teacher = teacher
            self.letter = self.getLetter()
            self.course = course
        def getLetter(self):
            try:
                if float(self.etm) >= 90 :
                    return "A"
                elif float(self.etm) >= 80 :
                    return "B"
                elif float(self.etm) >= 70 :
                    return "C"
                elif float(self.etm) >= 60 :
                    return "D"
                elif float(self.etm) >= 50 :
                    return "E"
                else:
                    return "F"
            except ValueError:
                return "MISSING"
            
                
        def __str__(self):
            return self.course + ": MTM " + str(self.mtm) + "| TEM " + str(self.final) + "| ETM " + str(self.etm) + "|" + str(self.average)