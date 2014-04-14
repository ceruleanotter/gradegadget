'''
Created on Aug 30, 2012
@author: Lyla

meant to create gradesheets from the outputted xls files of schooltool
'''


from mmap import mmap,ACCESS_READ
from xlrd import open_workbook,empty_cell
import os.path
import grade_gadget_methods
import prince_report_gen
from student_grade_data import Student
from course_section import Section
from user_inputs import ReportType, UserInput, AverageType


def generate_report(userInput) :
    #get the file paths
    school_excel_file = userInput.excel_file_location
    grade_location = os.path.dirname(userInput.excel_file_location)
    grades_excel_file = grade_location + "\\report_sheets_"+str(userInput.year)+"_"+str(userInput.term)+".xls"
    
    #open the file
    grades_workbook = open_workbook(grades_excel_file)
    school_workbook = open_workbook(school_excel_file)
    
    #getting all the sheets
    termgradesheet = grades_workbook.sheet_by_name(str(userInput.term))
    groupssheet = school_workbook.sheet_by_name("Groups")
    peoplesheet = school_workbook.sheet_by_name("Persons")
    coursesheet = school_workbook.sheet_by_name("Courses")
    
    sectionsheet = school_workbook.sheet_by_name("Sections")
    enrollmentsheet = school_workbook.sheet_by_name("SectionEnrollment")
    
    #get all of the students usernames based off of the group
    usernamesForSheets = grade_gadget_methods.getGroupMembers(userInput.group, groupssheet, userInput)
    
    #make a dictionary that matches the appropriate column types to their indexes in the sheet
    student_index_dic = grade_gadget_methods.makeIndexDict(peoplesheet, {"User Name":-1,"First Name":-1,"Last Name":-1,userInput.COMBO:-1, "Gender":-1,userInput.ADVISOR:-1})
    reportsheet_index_dic = grade_gadget_methods.makeIndexDict(termgradesheet,
                                                            {"Section ID":-1,"Student ID":-1,userInput.ETM:-1,userInput.FINAL:-1,userInput.COMMENT:-1,userInput.MTM:-1})
    sections_index_dic = grade_gadget_methods.makeIndexDict(sectionsheet,
                                                            {"School Year":-1,"Term":-1,"Title":-1,"Section ID":-1,"Instructors":-1,"Courses":-1})
    courses_index_dic = grade_gadget_methods.makeIndexDict(coursesheet,
                                                            {"School Year":-1,"ID":-1})
    
    #initalize course_section
    Section.initalize(coursesheet,courses_index_dic,userInput)
    
    
    #make some students
    students = {}
    for row in range (1,peoplesheet.nrows):
        curuser = peoplesheet.cell(row,student_index_dic["User Name"]).value
        #checking if the user is a student (or whatever group you're looking for)
        if curuser not in usernamesForSheets:
            continue
        students[curuser] = Student(peoplesheet.cell(row,student_index_dic["First Name"]).value,
                                 peoplesheet.cell(row,student_index_dic["Last Name"]).value,
                                 curuser,
                                 peoplesheet.cell(row,student_index_dic[userInput.COMBO]).value,
                                 peoplesheet.cell(row,student_index_dic[userInput.ADVISOR]).value)
        
    #this gets a dictionary that maps the teacher's username to the name on the report card
    teachers = grade_gadget_methods.getMapOfTeacherUsernameToGradeName(groupssheet, peoplesheet, student_index_dic, userInput)
    
    #maps the class id to a instance of section with all the correct info
    classes = grade_gadget_methods.makeClassesDic(sectionsheet, teachers, sections_index_dic, userInput)
    
    #calculate the average for courses
    if userInput.aveType == AverageType.Course:
        classes = grade_gadget_methods.calculateAveragesForCourses(classes, termgradesheet, reportsheet_index_dic,userInput)
    else:
        classes = grade_gadget_methods.calculateAveragesForSections(classes, termgradesheet, reportsheet_index_dic, userInput)
    
    #okay, now going to add the grade information
    #for some strange reason -1, seems to be the 4th column as well
    for row in range(1,termgradesheet.nrows):
        sectionID = termgradesheet.cell(row,reportsheet_index_dic["Section ID"]).value
        studentun = termgradesheet.cell(row,reportsheet_index_dic["Student ID"]).value
        
        final = termgradesheet.cell(row,reportsheet_index_dic[userInput.FINAL]).value
        etm = termgradesheet.cell(row,reportsheet_index_dic[userInput.ETM]).value
        mtm = termgradesheet.cell(row,reportsheet_index_dic[userInput.MTM]).value
        
        try:
            final = int(round(float(final)))
        except ValueError:
            final = "N/A"
    
        try:
            etm = int(round(float(etm)))
        except ValueError:
            etm = "N/A"
            
        try:
            mtm = int(round(float(mtm)))
        except ValueError:
            mtm = "N/A"        
        
        comment = False
        if (userInput.includeComments and reportsheet_index_dic[userInput.COMMENT] != -1):
            comment = termgradesheet.cell(row,reportsheet_index_dic[userInput.COMMENT]).value #trying this for comment
        
        try:
            students[studentun].addGrade(classes[sectionID], mtm, etm, final, comment)
            
        except KeyError:
            print "DOES NOT EXIST IN GROUP: " + studentun
    
    
    #now, caluclate GPAs
    grade_gadget_methods.calculateGPAs(students,userInput)
    grade_gadget_methods.setStudentReportYear(groupssheet, userInput, students)
    filetoprint = "No File"
    if(userInput.REPORT_TYPE == ReportType.Excel) :
        filetoprint = grade_gadget_methods.createExcel(students, userInput)
        #now we need to generate the file for the sheets
    else:
        filetoprint =  prince_report_gen.generatePrinceReports(students, userInput)
    
    #returns the file to print so the gui can say its' location
    return filetoprint
    
