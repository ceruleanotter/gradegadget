'''
Created on Aug 31, 2012

@author: Lyla
'''

from xlrd import empty_cell
from user_inputs import UserInput, ReportType
from course_section import Section
import csv
import datetime

SENIOR_4_SHEET = "Senior 4"
SENIOR_5_SHEET = "Senior 5"
SENIOR_6_SHEET = "Senior 6"

SENIOR_4_DISPLAY = "Senior 4"
SENIOR_5_DISPLAY = "Senior 5"
SENIOR_6_DISPLAY = "Senior 6"

def getGroupMembers(groupName, groupSheet, ui):
    """Given a valid group sheet, returns a list of the members"""
    #got to find which row the group states
    groupRow = -1
    #find where the group starts
    for row in range(groupSheet.nrows):
        if groupSheet.cell(row,1).value==groupName and groupSheet.cell(row+2,1).value==str(ui.year):
            groupRow = row
            break
    groupRow +=6 #this is how many farther down the actual list starts
    
    #keep adding names to the array until you hit a blank square
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
    return columnNamesDic


def getMapOfTeacherUsernameToGradeName(groupssheet,peoplesheet,student_index_dic, ui):
    """Changes the teacher's name to the name on the grade sheet, dependant on gender"""

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
    return teachers

def makeClassesDic(sectionSheet,teachers, sections_index_dic, ui):
    """Make objects for all the classes and put them in a dictionary"""

    classes = {}
    for row in range(1, sectionSheet.nrows):
        
        #need to check if the section is the correct year and everything
        if (sectionSheet.cell(row,sections_index_dic["Term"]).value == (str(ui.term)) and 
            sectionSheet.cell(row,sections_index_dic["School Year"]).value == str(ui.year)):
            sectionName = sectionSheet.cell(row,sections_index_dic["Title"]).value
            sectionID = sectionSheet.cell(row,sections_index_dic["Section ID"]).value
            
            try:
                instructor = teachers[sectionSheet.cell(row,sections_index_dic["Instructors"]).value.split(",")[0]]
            except KeyError:
                print "Error for "
                print sectionName
                instructor = "None"
            course = sectionSheet.cell(row,sections_index_dic["Courses"]).value
            
            #make a new class
            classes[sectionID] = Section(sectionID, sectionName, instructor, course)
            
    return classes

def calculateAveragesForSections(classes, termgradesheet, reportsheet_index_dic, ui):
    flag_missing=ui.flagMissing
    """Calculate the averages for classes based on section"""
    #differentiating between midterm and final
    if ui.REPORT_TYPE == ReportType.Final:
        gradeHeader = ui.ETM
    else:
        gradeHeader = ui.MTM
    
    #the class id for the class before the current one on the gradesheet
    prevclassID = termgradesheet.cell(1,reportsheet_index_dic["Section ID"]).value
    
    #set the current sum equal to this first class; catches if for some reason it's blank or not a numbe
    curMissingGrade = True
    cursum = 0
    curNumCounted = 0
    try:
        cursum = float(termgradesheet.cell(1,reportsheet_index_dic[gradeHeader]).value)
        curNumCounted = 1
        curMissingGrade = False
    except ValueError:
        curMissingGrade = True
        
    
    #starting from the second grade, check that it's the same class and then add it to the sum if so, otherwise calculate
    #the average for the class
    for row in range(2,termgradesheet.nrows):
        curclassID = termgradesheet.cell(row,reportsheet_index_dic["Section ID"]).value
        if curclassID != prevclassID :
            if curMissingGrade and flag_missing:
                classes[prevclassID].grade_average = "MISSING"
            elif int(curNumCounted) == 0:      
                classes[prevclassID].grade_average = "MISSING"                
            else:
                ave = int(round(float(cursum)/int(curNumCounted)))
                classes[prevclassID].grade_average = ave
                
            prevclassID = curclassID
            try:
                cursum = float(termgradesheet.cell(row,reportsheet_index_dic[gradeHeader]).value)
                curNumCounted = 1
                curMissingGrade = False
            except ValueError:
                curMissingGrade = True
                cursum = 0
                curNumCounted = 0
            continue
        
        prevclassID = curclassID
        try:
            curgrade = float(termgradesheet.cell(row,reportsheet_index_dic[gradeHeader]).value)
        except ValueError:
            curMissingGrade = True
            continue
        
        cursum = cursum + curgrade
        curNumCounted += 1
    return classes



def calculateAveragesForCourses(classes, termgradesheet, reportsheet_index_dic, ui):
    """Calculate the averages for classes based on course"""
    flag_missing=ui.flagMissing
    #get a unique list of all the courses, with the first place sighted

    if ui.REPORT_TYPE == ReportType.Final:
        gradeHeader = ui.ETM
    else:
        gradeHeader = ui.MTM
    
    courses = {}
    for row in range(1,termgradesheet.nrows):
        curcourseID = termgradesheet.cell(row,reportsheet_index_dic["Section ID"]).value.strip()
        curcourseID = curcourseID[0:4]
        if not(courses.has_key(curcourseID)):
            courses[curcourseID] = row
    
    #for each course, find the average
    for course in courses.keys():
        #start at the row where you first saw the course
        startRow = courses[course]
        sum = 0
        count = 0
        missingGrade = False
        for row in range(startRow,termgradesheet.nrows):
            curcourseID = termgradesheet.cell(row,reportsheet_index_dic["Section ID"]).value.strip()
            curcourseID = curcourseID[0:4]
            if course == curcourseID:
                try:
                    curgrade = float(termgradesheet.cell(row,reportsheet_index_dic[gradeHeader]).value)
                except ValueError:
                    missingGrade = True
                    #no need to keep checking if we just put missing; otherwise skip to the next occurence
                    if flag_missing:
                        break
                    else:
                        continue
                
                sum+=curgrade
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
    return classes

            
     
def calculateGPAs(students, ui):
    """Calls the calculate GPA on all students"""
    for s in students:
        students[s].calculateGPA((ui.REPORT_TYPE == ReportType.Final))

def setStudentReportYear(groupSheet, ui, students):
    s4_names = getGroupMembers(SENIOR_4_SHEET, groupSheet, ui)
    s5_names = getGroupMembers(SENIOR_5_SHEET, groupSheet, ui)
    s6_names = getGroupMembers(SENIOR_6_SHEET, groupSheet, ui)  
    students = students.values()
    for s in students:
        print s
        if s4_names.__contains__(s.username):
            s.currentYear = SENIOR_4_DISPLAY
        if s5_names.__contains__(s.username):
            s.currentYear = SENIOR_5_DISPLAY        
        if s6_names.__contains__(s.username):
            s.currentYear = SENIOR_6_DISPLAY        
        
      
def createExcel(students, ui):
    """Creates the GPA sheet"""
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

            
            
        