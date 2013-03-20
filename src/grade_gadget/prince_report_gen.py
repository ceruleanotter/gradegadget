'''
Created on Aug 31, 2012

@author: Lyla
'''
from user_inputs import *
from jinja2 import Environment, FileSystemLoader
import datetime
env = Environment(loader=FileSystemLoader(TEMPLATES_FOLDER))

def generatePrinceReports(students):
    print ":)"
    outer = env.get_template("outer_template.xhtml")
    #inner = env.get_template("inner_template.xhtml")
    sheets_html = outer.render(students=students,year=year,term=term)
    timenow = datetime.datetime.now()
    dayforfile = str(timenow.day) + "-" + str(timenow.month) + "-" + str(timenow.year) + "at" + str(timenow.hour) + "-" + str(timenow.minute) 
    f = open(HTML_OUTPUT_FOLDER+'report_sheets_for_'+str(group)+'_term_'+str(term)+'_'+str(year)+'generated_'+dayforfile+'.xhtml','w')
    f.write(sheets_html)


    
