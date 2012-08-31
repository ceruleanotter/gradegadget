'''
Created on Aug 31, 2012

@author: Lyla
'''

from xlrd import empty_cell
from course_section import Section
from user_inputs import *

def getGroupMembers(groupName, groupSheet):
    """Given a valid group sheet, returns a list of the members"""
    #got to find which row the group states
    groupRow = -1
    for row in range(groupSheet.nrows):
        if groupSheet.cell(row,1).value==groupName:
            groupRow = row
            break
    print groupRow
    groupRow +=6 #this is how many farther down the actual list starts
    
    names = []
    for row in range(groupRow,groupSheet.nrows):
        curcell = groupSheet.cell(row,0).value
        if curcell is empty_cell.value:
            break
        names.append(curcell)
    return names

def makeIndexDict(sheet, columnNamesDic):
    for col in range (sheet.ncols):
        cell = sheet.cell(0,col).value
        if cell in columnNamesDic:
            columnNamesDic[cell] = col
    print columnNamesDic
    return columnNamesDic


def getMapOfTeacherUsernameToGradeName(groupssheet,peoplesheet,student_index_dic):
    #get the teacher's usernames
    usernamesForTeachers = getGroupMembers(TEACHERS, groupssheet)
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
    print teachers
    return teachers

def makeClassesDic(sectionSheet,teachers):
    classes = {}
    for row in range(0, sectionSheet.nrows):
        if sectionSheet.cell(row,0).value == "Section Title":
            sectionName = sectionSheet.cell(row,1).value
            sectionID = sectionSheet.cell(row+1,1).value
            row += 1
            instructor ="None"
            #rapidly go through the rows to find the instructors or stop at the next section title
            while True :
                if sectionSheet.cell(row,0).value == "Section Title":
                    break
                if sectionSheet.cell(row,0).value == "Instructors":
                    instructor = teachers[sectionSheet.cell(row+1,0).value]
                    break
                row+=1
            classes[sectionID] = Section(sectionID, sectionName, instructor)
            print classes[sectionID]
    return classes

def calculateAveragesForClasses(classes, termgradesheet, reportsheet_index_dic):
    prevclassID = termgradesheet.cell(1,reportsheet_index_dic["Section ID"]).value
    cursum= int(termgradesheet.cell(1,reportsheet_index_dic[ETM]).value)
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
        curgrade = termgradesheet.cell(row,reportsheet_index_dic[ETM]).value
        prevclassID = curclassID
        if curgrade is empty_cell.value:
            curMissingGrade = True
            continue
        cursum = cursum + int(curgrade)
        curNumCounted += 1
    return classes