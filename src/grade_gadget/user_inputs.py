'''
Created on Aug 31, 2012

@author: Lyla
'''


class ReportType:
    Midterm, Final, Excel = range(3)



excel_file_location = "C:/Users/Lyla/Documents/GGAST/Technician/grade_generator/Python_Report_Generator/excel_sheets_from_schooltool/"
year = 2013
term = 3
group ="Students"


REPORT_TYPE = ReportType.Final
TEACHERS = "Teachers"
COMBO = "Combination"
ADVISOR = "Advisor"
ETM = "End of Term Marks for Term 3 2013 / End of Term Mark"
FINAL = "End of Term Marks for Term 3 2013 / Term Exam Mark"
MTM = "Midterm Marks Term for Term 3 2013 / Midterm Mark"
COMMENT = "End of Term Marks for Term 3 2013 / Student Comment"
TEMPLATES_FOLDER = "C:/Users/Lyla/Documents/GGAST/Technician/grade_generator/Python_Report_Generator/templates"
HTML_OUTPUT_FOLDER = "C:/Users/Lyla/Documents/GGAST/Technician/grade_generator/Python_Report_Generator/generated/"