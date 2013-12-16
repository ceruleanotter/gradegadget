'''
Created on Aug 31, 2012

@author: Lyla
'''
import os

class ReportType:
    Midterm, Final, Excel = range(3)
    reportTypesDic = {}
    reportTypesDic["Midterm"] = Midterm
    reportTypesDic["Final"] = Final
    reportTypesDic["Excel"] = Excel
    

class AverageType:
    Course, Section = range(2)
    aveTypesDic = {}
    aveTypesDic["Course"] = Course
    aveTypesDic["Section"] = Section

    

class UserInput(object):
    def __init__(self, export_location = "C:/Users/Lyla/Documents/GGAST/Technician/grade_generator/Python_Report_Generator/excel_sheets_from_schooltool/export.xls",
                 year=2013,
                 term="term-3",
                 tt = "Term 3",
                 group="Students",
                 repType=ReportType.Final,
                 aveType = AverageType.Course,
                 htmlOutputDir = "C:/Users/Lyla/Documents/GGAST/Technician/grade_generator/Python_Report_Generator/generated/",
                 includeComments = True):
        self.excel_file_location = export_location
        self.year = year
        self.term = term
        self.termTitle = tt
        self.group = group
        self.REPORT_TYPE = repType
        self.HTML_OUTPUT_FOLDER = htmlOutputDir
        self.aveType = aveType
        self.includeComments = includeComments
        
        
        self.TEACHERS = "Teachers"
        self.COMBO = "Combination"
        self.ADVISOR = "Advisor"
        self.ETM = "End of Term Marks for "+str(tt)+" "+str(year)+" / End of Term Mark"
        self.FINAL = "End of Term Marks for "+str(tt)+" "+str(year)+" / Term Exam Mark"
        self.MTM = "Midterm Marks Term for "+str(tt)+" "+str(year)+" / Midterm Mark"
        self.COMMENT = "End of Term Marks for "+str(tt)+" "+str(year)+" / Student Comment"
        self.TEMPLATES_FOLDER = os.path.dirname(self.excel_file_location) + "\\templates"
        print "just create a UI with " + self.TEMPLATES_FOLDER
 
    def setETM(self, etm):
        self.ETM = etm
        
    def setFINAL(self, final):
        self.FINAL = final
        
    def setMTM(self, mtm):
        self.MTM = mtm
            
    def setCOMMENT(self, comment):
        self.COMMENT = comment
            
    def setTEMPLATES_FOLDER(self, temp):
        self.TEMPLATES_FOLDER = temp
    
    def copy(self):
        
        newui = UserInput(export_location = self.excel_file_location,
                 year=self.year,
                 term=self.term,
                 tt = self.termTitle,
                 group= self.group,
                 repType= self.REPORT_TYPE,
                 aveType = self.aveType,
                 htmlOutputDir = self.HTML_OUTPUT_FOLDER)
        return newui
        