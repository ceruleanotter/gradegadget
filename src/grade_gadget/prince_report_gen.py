'''
Created on Aug 31, 2012

@author: Lyla
'''
from user_inputs import *
from jinja2 import Environment, FileSystemLoader
import datetime
import subprocess
#env = Environment(loader=FileSystemLoader(TEMPLATES_FOLDER))

# for ordering purposes


def generatePrinceReports(students,userInputs):
    env = Environment(loader=FileSystemLoader(userInputs.TEMPLATES_FOLDER))
    
    print ":)"
    
    #order the grades
    orderedStudents = sorted(students.values(),key=lambda student: student.lastName)

    
    outer = env.get_template("outer_template_sorted.xhtml")

    reportType=""
    
    
    if (userInputs.REPORT_TYPE == ReportType.Midterm):
        outer = env.get_template("outer_template_midterm.xhtml")
        reportType="Midterm"
    elif (userInputs.REPORT_TYPE == ReportType.Final):
        reportType = "Final"
    sheets_html = outer.render(students=orderedStudents,year=userInputs.year,term=userInputs.termTitle)
    
    timenow = datetime.datetime.now()

    
    dayforfile = str(timenow.day) + "-" + str(timenow.month) + "-" + str(timenow.year) + "at" + str(timenow.hour) + "-" + str(timenow.minute)
    
    filetoprint = userInputs.HTML_OUTPUT_FOLDER+reportType+"_Grades_For_"+userInputs.group+'_'+userInputs.termTitle+'_'+dayforfile+'.xhtml'
    print filetoprint
    f = open(filetoprint,'w')
    f.write(sheets_html.encode('utf-8'))
    
    return filetoprint



    
