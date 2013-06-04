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
        
    def addGrade(self,subject, mtm, etm, final, comment):        
        self.grades.append(self.Grade(subject.name, mtm, etm, final, subject.grade_average,
                                       subject.teacher, comment))

        
    
    def __str__(self):
        gradesoutput = ""
        for g in self.grades:
            gradesoutput += str(g)
            gradesoutput += "\n"
        return self.firstName + " " + self.lastName + ", Combo: " + self.combo + " Grades: " + gradesoutput
    
    class Grade(object):
        def __init__(self, subject, mtm, etm,final,ave,teacher,comment):
            self.subject = subject
            self.mtm = mtm
            self.etm = etm
            self.final = final
            self.average = ave
            self.comment = comment
            self.teacher = teacher
            self.letter = self.getLetter()
            
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
            return self.subject + ": MTM " + str(self.mtm) + "| TEM " + str(self.final) + "| ETM " + str(self.etm) + "|" + str(self.average)