'''
Created on Oct 2, 2012

@author: Lyla
'''
from student_mini import Student

if __name__ == '__main__':
    '''
Created on Aug 30, 2012
@author: Lyla

meant to create gradesheets from the outputted xls files of schooltool
'''
    
    

excel_file_location = "C:/Users/Lyla/Documents/GGAST/Technician/grade_generator/Python_Report_Generator/excel_sheets_from_lydia"

TEMPLATES_FOLDER = "C:/Users/Lyla/Documents/GGAST/Technician/grade_generator/Python_Report_Generator/templates_mini"
HTML_OUTPUT_FOLDER = "C:/Users/Lyla/Documents/GGAST/Technician/grade_generator/Python_Report_Generator/generated/"    

STUDENT_NAME = "NAMES"
COL_CLASS = 4
from mmap import mmap,ACCESS_READ
from xlrd import open_workbook,empty_cell
import os.path
from xlrd import empty_cell

from jinja2 import Environment, FileSystemLoader
import datetime

env = Environment(loader=FileSystemLoader(TEMPLATES_FOLDER))


def generatePrinceReports(students):
    print ":)"
    outer = env.get_template("outer_mini.xhtml")
    sheets_html = outer.render(students=students)
    timenow = datetime.datetime.now()
    dayforfile = str(timenow.day) + "-" + str(timenow.month) + "-" + str(timenow.year) + "at" + str(timenow.hour) + "-" + str(timenow.minute) 
    f = open(HTML_OUTPUT_FOLDER+'midtermsheets_'+dayforfile+'.xhtml','w')
    f.write(sheets_html)

s4 = excel_file_location + "/S4_final_2013.xlsx"
s5 = excel_file_location + "/S5_final_2013.xlsx"
s6 = excel_file_location + "/S6_final_2013.xlsx"
s4_workbook = open_workbook(s4)
s5_workbook = open_workbook(s5)
s6_workbook = open_workbook(s6)
gradesheets = {'Senior 4':(s4_workbook.sheet_by_name("Sheet1")),'Senior 5':(s5_workbook.sheet_by_name("Sheet1")), 'Senior 6':(s6_workbook.sheet_by_name("Sheet1"))}

title_row = -1
students = []

for sclass in gradesheets:
    sheet = gradesheets[sclass]
    for row in range(sheet.nrows):
        cur_class = 0
        id = sheet.cell(row,0).value
        name = sheet.cell(row,1).value
        
        if (id == empty_cell.value):
            if (name == STUDENT_NAME):
                 title_row = row
            continue #don't bother with rows that don't have students.
        combo = sheet.cell(row,2).value
        advisor = sheet.cell(row,3).value
        cur_col = COL_CLASS+cur_class*2
        cur_class_name = sheet.cell(title_row,cur_col).value
        #print "classname: " + str;
        classes = {}
        comments = {}
        try:
            while (cur_class_name != empty_cell.value):
                #if there is a grade for that class
                mark = sheet.cell(row,cur_col).value
                if (mark != empty_cell.value):
                    classes[cur_class_name] = int(mark)
                    comment = sheet.cell(row,(cur_col+1)).value
                    if (comment != empty_cell.value):
                        comments[cur_class_name] = comment
                cur_class += 1
                cur_col = COL_CLASS+cur_class*2
                cur_class_name = sheet.cell(title_row,cur_col).value
        except IndexError:
            print "done"
        print name 
        print classes
        print comments
        students.append(Student(name, sclass, advisor, combo, classes, comments))
generatePrinceReports(students)
        
        

#
##make some students
#students = {}
#for row in range (1,peoplesheet.nrows):
#    curuser = peoplesheet.cell(row,student_index_dic["User Name"]).value
#    if curuser not in usernamesForSheets:
#        continue
#    students[curuser] = Student(peoplesheet.cell(row,student_index_dic["First Name"]).value,
#                             peoplesheet.cell(row,student_index_dic["Last Name"]).value,
#                             curuser,
#                             peoplesheet.cell(row,student_index_dic[COMBO]).value)
##this gets a dictionary that maps the teacher's username to the name on the report card
#teachers = grade_gadget_methods.getMapOfTeacherUsernameToGradeName(groupssheet, peoplesheet, student_index_dic)
#
##maps the class id to a instance of section with all the correct info
#classes = grade_gadget_methods.makeClassesDic(sectionsheet, teachers)
#classes = grade_gadget_methods.calculateAveragesForClasses(classes, termgradesheet, reportsheet_index_dic)
#print reportsheet_index_dic
##need to come up with class averages
#for c in classes:
#    print classes[c]
#for s in students:
#    print s
##okay, now going to add the grade information
#for row in range(1,termgradesheet.nrows):
#    sectionID = termgradesheet.cell(row,reportsheet_index_dic["Section ID"]).value
#    studentun = termgradesheet.cell(row,reportsheet_index_dic["Student ID"]).value
#    final = termgradesheet.cell(row,reportsheet_index_dic[FINAL]).value
#    etm = termgradesheet.cell(row,reportsheet_index_dic[ETM]).value
#    ## WE WILL NEED SOMETHING FOR COMMENTS AND WHAT ABOUT MIDTERM?!?!?!
#    students[studentun].addGrade(classes[sectionID], "NEEDS TO BE IMPLEMENTED", etm, final, "NEEDS TO BE IMPLEMENTED")
#    print students[studentun]
#
##now we need to generate the file for the sheets
#prince_report_gen.generatePrinceReports(students)



#and command line run it through prince
