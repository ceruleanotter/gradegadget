'''
Created on Aug 31, 2012

@author: Lyla
'''
from user_inputs import *
from jinja2 import Environment, FileSystemLoader
env = Environment(loader=FileSystemLoader(TEMPLATES_FOLDER))

def generatePrinceReports(students):
    print ":)"
    template = env.get_template("outer_template.xhtml")
    print template.render(students=students,year=year,term=term)


    
