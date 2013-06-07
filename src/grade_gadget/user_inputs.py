'''
Created on Aug 31, 2012

@author: Lyla
'''


class ReportType:
    Midterm, Final = range(2)



excel_file_location = "C:/Users/Lyla/Documents/GGAST/Technician/grade_generator/Python_Report_Generator/excel_sheets_from_schooltool/"
year = 2013
term = 2
group ="Students"


REPORT_TYPE = ReportType.Midterm
TEACHERS = "Teachers"
COMBO = "Combination"
ADVISOR = "Advisor"
ETM = "Midterm Marks / Midterm Mark"
FINAL = "End of Term Marks for Term 1 2013 / Term Exam Mark"
MTM = "End of Term Marks for Term 1 2013 / Mid Term Mark"
COMMENT = "End of Term Marks for Term 1 2013 / Student Comment"
TEMPLATES_FOLDER = "C:/Users/Lyla/Documents/GGAST/Technician/grade_generator/Python_Report_Generator/templates"
HTML_OUTPUT_FOLDER = "C:/Users/Lyla/Documents/GGAST/Technician/grade_generator/Python_Report_Generator/generated/"