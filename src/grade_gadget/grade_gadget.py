'''
Created on Aug 30, 2012
@author: Lyla

meant to create gradesheets from the outputted xls files of schooltool
'''
from mmap import mmap,ACCESS_READ
from xlrd import open_workbook,empty_cell
import os.path
from student_grade_data import Student
from course_section import Section
excel_file_location = "C:/Users/Lyla/Documents/GGAST/Technician/grade_generator/Python_Report_Generator/excel_sheets_from_schooltool/"

year = 2012
term = 2
group ="Students"

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
sectionsheet = school_workbook.sheet_by_name("Sections " +str(year) + " " + "term-" + str(term))
print sectionsheet


#go through groupssheet and get the list of student
studentGroupRow = -1
for row in range(groupssheet.nrows):
    if groupssheet.cell(row,1).value==group:
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
info_cols= {"User Name":-1,"First Name":-1,"Last Name":-1,"Ethnicity":-1, "Gender":-1}
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

#get a list of teachers, won't wory if not in the teacher group, could make this a method later!!!
teacherGroupRow = -1
for row in range(groupssheet.nrows):
    if groupssheet.cell(row,1).value=="Teachers":
        teacherGroupRow = row
        break
print teacherGroupRow
teacherGroupRow +=6 #this is how many farther down the actual list starts

#also, could combine this part with the student part so it doesn't go through the whole list twice
teacherun = []
for row in range(teacherGroupRow,groupssheet.nrows):
    curcell = groupssheet.cell(row,0).value
    if curcell is empty_cell.value:
        break
    teacherun.append(curcell)

print teacherun
teachers = {}
for row in range (1,peoplesheet.nrows):
    curuser = peoplesheet.cell(row,info_cols["User Name"]).value
    if curuser not in teacherun:
        continue
    name = ""
    if peoplesheet.cell(row,info_cols["Gender"]).value == "female":
        name = "Ms."+peoplesheet.cell(row,info_cols["First Name"]).value
    else:
        name = "Mr."+peoplesheet.cell(row,info_cols["First Name"]).value
    teachers[curuser] = name
    
print teachers
#need to come up with a mapping of id to subject
classes = {}
for row in range(0, sectionsheet.nrows):
    if sectionsheet.cell(row,0).value == "Section Title":
        sectionName = sectionsheet.cell(row,1).value
        sectionID = sectionsheet.cell(row+1,1).value
        row += 1
        instructor ="None"
        #rapidly go through the rows to find the instructors or stop at the next section title
        while True :
            if sectionsheet.cell(row,0).value == "Section Title":
                break
            if sectionsheet.cell(row,0).value == "Instructors":
                instructor = teachers[sectionsheet.cell(row+1,0).value]
                break
            row+=1
        classes[sectionID] = Section(sectionID, sectionName, instructor)
        print classes[sectionID]

#come up with the nice colum name to colum mapping for the report sheet
grade_cols= {"Section ID":-1,"Student ID":-1,"Final Grades Term 2 / End of Term Mark":-1,"Final Grades Term 2 / Final Test Grade":-1}
for col in range (termgradesheet.ncols):
    cell = termgradesheet.cell(0,col).value
    if cell in grade_cols:
        grade_cols[cell] = col
        
print grade_cols
#need to come up with class averages

#okay, now going to add the grade information



#for s in wb.sheets():
#    print 'Sheet:',s.name
#    for row in range(s.nrows):
#        values = []
#        for col in range(s.ncols):
#            values.append(s.cell(row,col).value)
#        print ','.join(values)