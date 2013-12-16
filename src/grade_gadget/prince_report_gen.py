'''
Created on Aug 31, 2012

@author: Lyla
'''
from user_inputs import *
from jinja2 import Environment, FileSystemLoader
import datetime
#env = Environment(loader=FileSystemLoader(TEMPLATES_FOLDER))

# for ordering purposes


def generatePrinceReports(students,userInputs):
    print userInputs.TEMPLATES_FOLDER
    env = Environment(loader=FileSystemLoader(userInputs.TEMPLATES_FOLDER))
    
    print ":)"
    
    #order the grades
    orderedStudents = sorted(students.values(),key=lambda student: student.lastName)

    #print orderedStudents

      
    
    outer = env.get_template("outer_template_sorted.xhtml")
    if (userInputs.REPORT_TYPE == ReportType.Midterm):
        outer = env.get_template("outer_template_midterm.xhtml")
    
    #inner = env.get_template("inner_template.xhtml")
    sheets_html = outer.render(students=orderedStudents,year=userInputs.year,term=userInputs.termTitle)
    
    timenow = datetime.datetime.now()
    dayforfile = str(timenow.day) + "-" + str(timenow.month) + "-" + str(timenow.year) + "at" + str(timenow.hour) + "-" + str(timenow.minute)
    filetoprint = userInputs.HTML_OUTPUT_FOLDER+'report_sheets_for_'+str(userInputs.group)+'_term_'+str(userInputs.term)+'_'+str(userInputs.year)+'generated_'+dayforfile+'.xhtml' 
    f = open(filetoprint,'w')
    f.write(sheets_html.encode('utf-8'))
    return filetoprint

    
