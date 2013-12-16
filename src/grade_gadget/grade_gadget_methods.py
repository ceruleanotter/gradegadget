'''
Created on Aug 31, 2012

@author: Lyla
'''

from xlrd import empty_cell
from user_inputs import UserInput
from course_section import Section
import csv
import datetime

def getGroupMembers(groupName, groupSheet, ui):
    """Given a valid group sheet, returns a list of the members"""
    #got to find which row the group states
    groupRow = -1

    for row in range(groupSheet.nrows):
        if groupSheet.cell(row,1).value==groupName and groupSheet.cell(row+2,1).value==str(ui.year):
            groupRow = row
            break
    #print groupRow
    groupRow +=6 #this is how many farther down the actual list starts
    
    names = []
    for row in range(groupRow,groupSheet.nrows):
        curcell = groupSheet.cell(row,0).value
        if curcell is empty_cell.value:
            break
        names.append(curcell)
    return names

def makeIndexDict(sheet, columnNamesDic):
    """Given a valid worksheet, returns a dictionary matching the column headers with their numeric location"""
    for col in range (sheet.ncols):
        cell = sheet.cell(0,col).value
        if cell in columnNamesDic:
            columnNamesDic[cell] = col
    #print columnNamesDic
    return columnNamesDic


def getMapOfTeacherUsernameToGradeName(groupssheet,peoplesheet,student_index_dic, ui):
    #get the teacher's usernames
    usernamesForTeachers = getGroupMembers(ui.TEACHERS, groupssheet, ui)
    teachers = {}
    for row in range (1,peoplesheet.nrows):
        curuser = peoplesheet.cell(row,student_index_dic["User Name"]).value
        if curuser not in usernamesForTeachers:
            continue
        name = ""
        if peoplesheet.cell(row,student_index_dic["Gender"]).value == "female":
            name = "Ms."+peoplesheet.cell(row,student_index_dic["First Name"]).value
        else:
            name = "Mr."+peoplesheet.cell(row,student_index_dic["First Name"]).value
        teachers[curuser] = name
    #print teachers
    return teachers

def makeClassesDic(sectionSheet,teachers, sections_index_dic, ui):
    classes = {}
    for row in range(1, sectionSheet.nrows):
        
        #need to check if the section is the correct year and everything
        if (sectionSheet.cell(row,sections_index_dic["Term"]).value == (str(ui.term)) and 
            sectionSheet.cell(row,sections_index_dic["School Year"]).value == str(ui.year)):
            sectionName = sectionSheet.cell(row,sections_index_dic["Title"]).value
            sectionID = sectionSheet.cell(row,sections_index_dic["Section ID"]).value
            instructor = teachers[sectionSheet.cell(row,sections_index_dic["Instructors"]).value.split(",")[0]]
            course = sectionSheet.cell(row,sections_index_dic["Courses"]).value
        #goes to every section, get the name, id, instructors, title
        #need to be changed
        
#        if sectionSheet.cell(row,0).value == "Section Title":
#            sectionName = sectionSheet.cell(row,1).value
#            sectionID = sectionSheet.cell(row+1,1).value
#            row += 1
#            instructor ="None"
#            #rapidly go through the rows to find the instructors or stop at the next section title
#            while True :
#                if sectionSheet.cell(row,0).value == "Section Title":
#                    break
#                if sectionSheet.cell(row,0).value == "Instructors":
#                    instructor = teachers[sectionSheet.cell(row+1,0).value]
#                    break
#                row+=1
            classes[sectionID] = Section(sectionID, sectionName, instructor, course)
            #print classes[sectionID]
    return classes

def calculateAveragesForSections(classes, termgradesheet, reportsheet_index_dic, ui):
    prevclassID = termgradesheet.cell(1,reportsheet_index_dic["Section ID"]).value
    cursum= int(termgradesheet.cell(1,reportsheet_index_dic[ui.ETM]).value)
    curNumCounted = 1
    curMissingGrade = False
    for row in range(2,termgradesheet.nrows):
        curclassID = termgradesheet.cell(row,reportsheet_index_dic["Section ID"]).value
        if curclassID != prevclassID :
            if curMissingGrade:
                classes[prevclassID].grade_average = "MISSING"            
            else:
                ave = int(cursum)/int(curNumCounted)
                classes[prevclassID].grade_average = ave
            cursum = 0
            curNumCounted = 0
            curMissingGrade = False
            prevclassID = curclassID
            continue
        #print termgradesheet.cell(row,reportsheet_index_dic["Final Grades Term 2 / End of Term Mark"]).value
        curgrade = termgradesheet.cell(row,reportsheet_index_dic[ui.ETM]).value
        prevclassID = curclassID
        if curgrade is empty_cell.value:
            curMissingGrade = True
            continue
        cursum = cursum + float(curgrade)
        curNumCounted += 1
    return classes



def calculateAveragesForCourses(classes, termgradesheet, reportsheet_index_dic, ui,flag_missing=True):
    #get a unique list of all the courses, with the first place sighted
    #print "classes is " + str(classes)
    #print "termgradesheet is " + str(termgradesheet)
    #print "reportsheet_index_dic " + str(reportsheet_index_dic)
    #print "ui is " + str(ui)
    #print "flag_missing is " + str(flag_missing)
    
    courses = {}
    for row in range(1,termgradesheet.nrows):
        curcourseID = termgradesheet.cell(row,reportsheet_index_dic["Section ID"]).value.strip()
        curcourseID = curcourseID[0:4]
        if not(courses.has_key(curcourseID)):
            courses[curcourseID] = row
    # print courses
    #for each course, find the average
    for course in courses.keys():
        startRow = courses[course]
        sum = 0
        count = 0
        missingGrade = False
        for row in range(startRow,termgradesheet.nrows):
            curcourseID = termgradesheet.cell(row,reportsheet_index_dic["Section ID"]).value.strip()
            curcourseID = curcourseID[0:4]
            if course == curcourseID:
                curgrade = termgradesheet.cell(row,reportsheet_index_dic[ui.ETM]).value
                if curgrade is empty_cell.value:
                    missingGrade = True
                    break
            
                sum+=float(curgrade)
                count+=1
        if flag_missing and missingGrade:
            courses[course] = "MISSING"
        else:
            if int(count) == 0:
                courses[course] = "MISSING"                
            else:
                courses[course] = int(round((float(sum)/int(count))))
 
    #match section with course average
    for c in classes.keys():
        classCourse = c[0:4]
        classes[c].grade_average = courses[classCourse]
        #print classes[c]
    return classes

            
     
def calculateGPAs(students):
    for s in students:
        students[s].calculateGPA()
        
def createExcel(students, ui):
    #print students
    student_gpas = [];
    student_gpas.append(("First Name", "Last Name", "GPA for " + str(ui.term) + " " + str(ui.year)))
    for s in students:
        student = students[s]
        student_gpas.append([student.firstName,student.lastName,student.gpa])
    timenow = datetime.datetime.now()
    dayforfile = str(timenow.day) + "-" + str(timenow.month) + "-" + str(timenow.year) + "at" + str(timenow.hour) + "-" + str(timenow.minute) 
    filetoprint = ui.HTML_OUTPUT_FOLDER+'gpas_for_'+str(ui.group)+"_"+str(ui.term)+'_'+str(ui.year)+'generated_'+dayforfile+'.csv'
    with open(filetoprint,'w') as gpa_csv:
        writer = csv.writer(gpa_csv)
        writer.writerows(student_gpas)
    return filetoprint

            
            
        