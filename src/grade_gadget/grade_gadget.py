'''
Created on Aug 30, 2012
@author: Lyla

meant to create gradesheets from the outputted xls files of schooltool
'''
from mmap import mmap,ACCESS_READ
from xlrd import open_workbook,empty_cell
import os.path
from student_grade_data import Student
excel_file_location = "C:/Users/Lyla/Documents/GGAST/Technician/grade_generator/Python_Report_Generator/excel_sheets_from_schooltool/"

year = 2012
term = 2

grades_excel_file = excel_file_location + "report_sheets_"+str(year)+".xls"
school_excel_file = excel_file_location + "export.xls"
grades_workbook = open_workbook(grades_excel_file)
school_workbook = open_workbook(school_excel_file)

termgradesheet = grades_workbook.sheet_by_name("term-"+str(term))
print termgradesheet
groupssheet = school_workbook.sheet_by_name("Groups")
print groupssheet
peoplesheet = school_workbook.sheet_by_name("Persons")
print peoplesheet

#go through groupssheet and get the list of student
studentGroupRow = -1
for row in range(groupssheet.nrows):
    if groupssheet.cell(row,1).value=="Students":
        studentGroupRow = row
        break
print studentGroupRow
studentGroupRow +=6 #this is how many farther down the actual list starts

usernamesForSheets = []
for row in range(studentGroupRow,groupssheet.nrows):
    curcell = groupssheet.cell(row,0).value
    if curcell is empty_cell.value:
        break
    usernamesForSheets.append(curcell)


#silly testing
assert usernamesForSheets[0] == "abingeneyes"
assert usernamesForSheets[len(usernamesForSheets)-1] == "wihogorax"
#done silly testing

#make a dictionary that matches the appropriate column types to their indexes in the sheet
info_cols= {"User Name":-1,"First Name":-1,"Last Name":-1,"Ethnicity":-1}
for col in range (peoplesheet.ncols):
    cell = peoplesheet.cell(0,col).value
    if cell in info_cols:
        info_cols[cell] = col
        
print info_cols
    
students = []
#make some students
for row in range (1,peoplesheet.nrows):
    curuser = peoplesheet.cell(row,info_cols["User Name"]).value
    if curuser not in usernamesForSheets:
        continue
    students.append(Student(peoplesheet.cell(row,info_cols["First Name"]).value,
                             peoplesheet.cell(row,info_cols["Last Name"]).value,
                             curuser,
                             peoplesheet.cell(row,info_cols["Ethnicity"]).value))



#for s in wb.sheets():
#    print 'Sheet:',s.name
#    for row in range(s.nrows):
#        values = []
#        for col in range(s.ncols):
#            values.append(s.cell(row,col).value)
#        print ','.join(values)