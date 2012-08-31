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

from user_inputs import *
#this stuff should be collected, maybe as part of the gui

grades_excel_file = excel_file_location + "report_sheets_"+str(year)+".xls"
school_excel_file = excel_file_location + "export.xls"
grades_workbook = open_workbook(grades_excel_file)
school_workbook = open_workbook(school_excel_file)

#getting all the sheets
termgradesheet = grades_workbook.sheet_by_name("term-"+str(term))
groupssheet = school_workbook.sheet_by_name("Groups")
peoplesheet = school_workbook.sheet_by_name("Persons")
sectionsheet = school_workbook.sheet_by_name("Sections " +str(year) + " " + "term-" + str(term))

#get all of the students usernames
usernamesForSheets = grade_gadget_methods.getGroupMembers(group, groupssheet)

#make a dictionary that matches the appropriate column types to their indexes in the sheet
student_index_dic = grade_gadget_methods.makeIndexDict(peoplesheet, {"User Name":-1,"First Name":-1,"Last Name":-1,COMBO:-1, "Gender":-1})
reportsheet_index_dic = grade_gadget_methods.makeIndexDict(termgradesheet,
                                                           {"Section ID":-1,"Student ID":-1,ETM:-1,FINAL:-1})

#make some students
students = {}
for row in range (1,peoplesheet.nrows):
    curuser = peoplesheet.cell(row,student_index_dic["User Name"]).value
    if curuser not in usernamesForSheets:
        continue
    students[curuser] = Student(peoplesheet.cell(row,student_index_dic["First Name"]).value,
                             peoplesheet.cell(row,student_index_dic["Last Name"]).value,
                             curuser,
                             peoplesheet.cell(row,student_index_dic[COMBO]).value)
#this gets a dictionary that maps the teacher's username to the name on the report card
teachers = grade_gadget_methods.getMapOfTeacherUsernameToGradeName(groupssheet, peoplesheet, student_index_dic)

#maps the class id to a instance of section with all the correct info
classes = grade_gadget_methods.makeClassesDic(sectionsheet, teachers)
classes = grade_gadget_methods.calculateAveragesForClasses(classes, termgradesheet, reportsheet_index_dic)
print reportsheet_index_dic
#need to come up with class averages
for c in classes:
    print classes[c]
for s in students:
    print s
#okay, now going to add the grade information
for row in range(1,termgradesheet.nrows):
    sectionID = termgradesheet.cell(row,reportsheet_index_dic["Section ID"]).value
    studentun = termgradesheet.cell(row,reportsheet_index_dic["Student ID"]).value
    final = termgradesheet.cell(row,reportsheet_index_dic[FINAL]).value
    etm = termgradesheet.cell(row,reportsheet_index_dic[ETM]).value
    ## WE WILL NEED SOMETHING FOR COMMENTS AND WHAT ABOUT MIDTERM?!?!?!
    students[studentun].addGrade(classes[sectionID], "NEEDS TO BE IMPLEMENTED", etm, final, "NEEDS TO BE IMPLEMENTED")
    print students[studentun]

#now we need to generate the file for the sheets
prince_report_gen.generatePrinceReports(students)



#and command line run it through prince
