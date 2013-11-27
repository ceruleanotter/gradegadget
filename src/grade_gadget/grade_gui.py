##---------------------------------------------------------------------------
#
## This is how you pre-establish a file filter so that the dialog
## only shows the extension(s) you want it to.
#wildcard = "Python source (*.py)|*.py|"     \
#           "Compiled Python (*.pyc)|*.pyc|" \
#           "SPAM files (*.spam)|*.spam|"    \
#           "Egg file (*.egg)|*.egg|"        \
#           "All files (*.*)|*.*"

#---------------------------------------------------------------------------

import wx
import os
import datetime
from xlrd import open_workbook, biffh
from user_inputs import ReportType, AverageType
from user_inputs import UserInput
from grade_gadget import generate_report
import pickle

class TermTuple:
    def __init__(self, term, termTitle):
        self.term = term
        self.termTitle = termTitle
    
    
class GradeGadgetFrame(wx.Frame):
    
    """
    This is GradeGadgetFrame.  It contains everything for the grade gadget gui.
    """
    PEACEFUL_MESSAGE = "Welcome to The Gashora Grade Gadget Report Generator"
    INFORMATIONAL_MESSAGE = ("IF NO CHANGES NEED TO BE MADE LEAVE THIS BLANK\n\n"
                             "These are advanced options; only to be changed in rare situations. \n"
                             "The Excel Headings refers to the excel file with the grades. This program "
                             "tries to guess the headings automatically using the term and year you enter. "
                             "For example, for midterm grades, term 2, year 2013, it generates the heading:\n\n"
                             "Midterm Marks Term for Term 2 2013 / Midterm Mark\n\n"
                             "Only change this if there is an error in the headings of your Excel Grades file\n\n"
                             "The Template folder is the folder where your html template files are, you "
                             "might need to change this if the style of the reports needs to change or if you "
                             "move your files")
    FRAME_WIDTH = 600
    FRAME_HEIGHT = 500
    def __init__(self, *args, **kwargs):
        super(GradeGadgetFrame, self).__init__(*args, **kwargs) 
            
        self.InitUI()
        
    def InitUI(self):
        

        
        self.currentDirectory = os.getcwd()
        self.SetSize((GradeGadgetFrame.FRAME_WIDTH, GradeGadgetFrame.FRAME_HEIGHT))
        self.SetTitle('Gashora Grade Gadget -- Report Generator')
        self.parentNotebook = wx.Notebook(self, -1, size=(GradeGadgetFrame.FRAME_WIDTH,GradeGadgetFrame.FRAME_HEIGHT), style=
                             wx.BK_DEFAULT
                             #wx.BK_TOP 
                             #wx.BK_BOTTOM
                             #wx.BK_LEFT
                             #wx.BK_RIGHT
                             # | wx.NB_MULTILINE
                             )        

        
        
        mainpanel = wx.Panel(self.parentNotebook)
        self.parentNotebook.AddPage(mainpanel, "Main Options")


        vbox = wx.BoxSizer(wx.VERTICAL)
        row1 = wx.BoxSizer(wx.HORIZONTAL)
        row2 = wx.BoxSizer(wx.HORIZONTAL)
        row3 = wx.BoxSizer(wx.HORIZONTAL)        
        row4 = wx.BoxSizer(wx.HORIZONTAL)    
        row5 = wx.BoxSizer(wx.HORIZONTAL)    
        row6 = wx.BoxSizer(wx.HORIZONTAL)    
        row7 = wx.BoxSizer(wx.HORIZONTAL)
        
        #row1                   
        box_chooseExport = wx.StaticBox(mainpanel, label='Choose School Export File');
        sb_chooseExport = wx.StaticBoxSizer(box_chooseExport, wx.HORIZONTAL)
        
        self.text_ctrl_export = wx.TextCtrl(mainpanel, -1, "click browse", style=wx.TE_READONLY, name="Export File Path")
        button_browse_export = wx.Button(mainpanel, label="Browse")
        
        sb_chooseExport.Add(self.text_ctrl_export,1,flag=wx.ALL|wx.EXPAND, border=5)
        sb_chooseExport.Add(button_browse_export,flag=wx.ALL, border=5)        
        
        row1.Add(sb_chooseExport,1, flag=wx.ALL|wx.EXPAND, border=5)
        
        
        
        #row2
        text_term = wx.StaticText(mainpanel, label='Term');
        self.combo_term = wx.ComboBox(mainpanel, choices=[],style=wx.CB_READONLY, name="Term Selection")
        row2.Add(text_term,flag=wx.ALL|wx.EXPAND, border=5)
        row2.Add(self.combo_term,flag=wx.ALL|wx.EXPAND, border=5)
        
        self.text_year = wx.StaticText(mainpanel, label='Year');
        self.year = str(datetime.datetime.now().year)
        print self.year #!need to add change year functionality
        self.spin_year = wx.SpinCtrl(mainpanel, value=self.year)                
        self.spin_year.SetRange(2010,2500)
        row2.Add(self.text_year,flag=wx.ALL|wx.EXPAND, border=5)        
        row2.Add(self.spin_year,flag=wx.ALL|wx.EXPAND, border=5)  
                
        #row3
        text_group = wx.StaticText(mainpanel, label='Group');
        self.combo_group = wx.ComboBox(mainpanel, choices=[], style=wx.CB_READONLY, name="Group Selection")
        row3.Add(text_group,flag=wx.ALL|wx.EXPAND, border=5)  
        row3.Add(self.combo_group,flag=wx.ALL|wx.EXPAND, border=5)  
                
        #row4
        text_type = wx.StaticText(mainpanel, label='Type of Report');
        row4.Add(text_type,flag=wx.ALL|wx.EXPAND, border=5)  
        
        first=True
        
        self.radio_buttons_report = []
        for rt in ReportType.reportTypesDic.keys():
            if first:
                cur_rb = wx.RadioButton(mainpanel, label=rt, style=wx.RB_GROUP)
                first = False
            else:
                cur_rb = wx.RadioButton(mainpanel, label=rt)
            row4.Add(cur_rb,flag=wx.ALL|wx.EXPAND, border=5)
            self.radio_buttons_report.append(cur_rb)
        
        
        #row5
        text_ave = wx.StaticText(mainpanel, label='Average Calculation Style');

        row5.Add(text_ave,flag=wx.ALL|wx.EXPAND, border=5)  
        
        self.radio_buttons_average = []
        first = True
        for at in AverageType.aveTypesDic.keys():
            if first:
                cur_rb = wx.RadioButton(mainpanel, label=at, style=wx.RB_GROUP)
                first = False
            else:
                cur_rb = wx.RadioButton(mainpanel, label=at)
            row5.Add(cur_rb,flag=wx.ALL|wx.EXPAND, border=5)
            self.radio_buttons_average.append(cur_rb) 
        
        #row6                
#        box_output = wx.StaticBox(mainpanel, label='Output Folder');
#        sb_output = wx.StaticBoxSizer(box_output, wx.HORIZONTAL)
#        
#        self.text_ctrl_output = wx.TextCtrl(mainpanel, -1, self.currentDirectory, style=wx.TE_READONLY, name="Output Folder Path" )
#        button_browse_output = wx.Button(mainpanel, label="Browse")
#        
#        sb_output.Add(self.text_ctrl_output,1,flag=wx.ALL,border=5)
#        sb_output.Add(button_browse_output,flag=wx.ALL,border=5)
#        
#        row6.Add(sb_output,1, flag=wx.ALL|wx.EXPAND, border=5)
#        
        
        #line
        line = wx.StaticLine(mainpanel)
        
        #row7
        button_generate = wx.Button(mainpanel, label="Generate Report")
        row7.Add(button_generate,flag=wx.BOTTOM|wx.TOP, border=5)        
        
        #static error text
        
        self.error_text = wx.StaticText(mainpanel, label=self.PEACEFUL_MESSAGE)
        
        
        vbox.Add(row1, flag=wx.EXPAND)
        vbox.Add(row2, flag=wx.EXPAND)
        vbox.Add(row3, flag=wx.EXPAND)
        vbox.Add(row4, flag=wx.EXPAND)
        vbox.Add(row5, flag=wx.EXPAND)        
        vbox.Add(row6, flag=wx.EXPAND)
       
        vbox.Add(line, flag=wx.EXPAND|wx.BOTTOM, border=10)
        
        vbox.Add(row7, flag=wx.ALIGN_CENTER)        
        
        vbox.Add(self.error_text, flag= wx.ALIGN_BOTTOM)        
        
        
        mainpanel.SetSizer(vbox)
        
        #Event Stuff
        button_browse_export.Bind(wx.EVT_BUTTON, self.onBrowseExport)
       
        #button_browse_output.Bind(wx.EVT_BUTTON, self.onBrowseOutputFolder)        
        button_generate.Bind(wx.EVT_BUTTON, self.onGenerate)
        self.spin_year.Bind(wx.EVT_SPIN, self.onSpinYear)
        
        
        #####ADVANCED OPTIONS######
        advancedpanel = wx.Panel(self.parentNotebook,)
        self.parentNotebook.AddPage(advancedpanel, "Advanced Options")

        
        
        
        
        avbox = wx.BoxSizer(wx.VERTICAL)
        arow1 = wx.BoxSizer(wx.HORIZONTAL)
        arow2 = wx.BoxSizer(wx.HORIZONTAL)
        
        #row1                   
        a_box_excel_headings = wx.StaticBox(advancedpanel, label='Change Excel Headings');
        a_sb_excel_headings = wx.StaticBoxSizer(a_box_excel_headings, wx.VERTICAL)
        
        self.a_text_control_etm = self.makeAdvancedRewriteHeadingBox("ETM", advancedpanel, a_sb_excel_headings)
        self.a_text_control_final = self.makeAdvancedRewriteHeadingBox("Final", advancedpanel, a_sb_excel_headings)
        self.a_text_control_mtm = self.makeAdvancedRewriteHeadingBox("MTM", advancedpanel, a_sb_excel_headings)
        self.a_text_control_comment = self.makeAdvancedRewriteHeadingBox("Comment", advancedpanel, a_sb_excel_headings)
        
        self.headings_list =[self.a_text_control_comment,self.a_text_control_mtm,self.a_text_control_final,self.a_text_control_etm]

        
        
        a_box_template_location = wx.StaticBox(advancedpanel, label = "Change Templates Folder")                                                                                     
        a_sb_template_location = wx.StaticBoxSizer(a_box_template_location, wx.HORIZONTAL)
        self.a_text_control_template_location = wx.TextCtrl(advancedpanel, -1,"", style=wx.TE_READONLY)
        a_button_browse_template_location = wx.Button(advancedpanel, label="Browse", name="Template Folder Path")

        a_sb_template_location.Add(self.a_text_control_template_location, 1, flag=wx.EXPAND|wx.ALL, border=5)
        a_sb_template_location.Add(a_button_browse_template_location, flag=wx.ALL, border=5)
        
        self.informational_text = wx.StaticText(advancedpanel, label=self.INFORMATIONAL_MESSAGE)
        self.informational_text.Wrap(GradeGadgetFrame.FRAME_WIDTH-10)
        
        
        arow1.Add(a_sb_excel_headings,1, flag=wx.ALL|wx.EXPAND, border=5)
        arow2.Add(a_sb_template_location,1,flag=wx.ALL|wx.EXPAND, border=5)
        avbox.Add(arow1, flag=wx.EXPAND)
        avbox.Add(arow2, flag=wx.EXPAND)
        avbox.Add(self.informational_text, flag=wx.EXPAND)
        
        advancedpanel.SetSizer(avbox)
        
        
        
        
        self.Centre()
        self.Show(True)
        
        
    def onBrowseExport(self, event):
            filters = 'Excel files from SchoolTool (*.xls)|*.xls'

            dialog = wx.FileDialog(self,
                                   message="Choose an export.xls file",
                                   defaultDir = self.currentDirectory,
                                   defaultFile = "",
                                   wildcard = filters,
                                   style=wx.OPEN | wx.CHANGE_DIR
                                   )
            if dialog.ShowModal() == wx.ID_OK:
                path = dialog.GetPath()
                #some code in here to call a grade gadget method to grab the groups
                self.setGroups(path)
                self.setTerms(path)
                #
                self.text_ctrl_export.SetLabel(path)
                print path
            dialog.Destroy()
            
    def setGroups(self, exportfilepath):
        try:
            school_workbook = open_workbook(exportfilepath)
            groupssheet = school_workbook.sheet_by_name("Groups")
            groupsList = []
            for row in range(groupssheet.nrows):
                if groupssheet.cell(row,0).value=="Group Title" and groupssheet.cell(row+2,1).value==str(self.year):
                    groupsList.append(groupssheet.cell(row,1).value)
            #remove groups that will never have report cards
            try:
                groupsList.remove("School Administrators")
                groupsList.remove("Clerks")
                groupsList.remove("Teachers")
                groupsList.remove("Site Managers")
            except ValueError:
                print "Values not in list"
            self.combo_group.Clear()
            self.combo_group.AppendItems(groupsList)
            print groupsList
        except (IOError, biffh.XLRDError):
            print "Can't open the file to find the groups"
            self.combo_group.Clear()    
            
    def setTerms(self, exportfilepath):
        try:
            school_workbook = open_workbook(exportfilepath)
            termsheet = school_workbook.sheet_by_name("Terms")
            #termList = []
            self.combo_term.Clear()
            for row in range(termsheet.nrows):
                if termsheet.cell(row,0).value==str(self.year):
                    t= TermTuple(termsheet.cell(row,1).value, termsheet.cell(row,2).value)
                    #termList.append(t.term,t)
                    self.combo_term.Append(t.termTitle,t)
            
            
        except (IOError, biffh.XLRDError):
            print "Can't open the file to find the terms"
            self.combo_term.Clear()                   

 



#    def onBrowseOutputFolder(self, event):
#            print "output pressed"
#            dialog = wx.DirDialog(self,
#                                   message="Choose a directory",
#                                   style=wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST| wx.DD_CHANGE_DIR,
#                                   defaultPath=self.currentDirectory
#                                   )
#            
#            if dialog.ShowModal() == wx.ID_OK:
#                path = dialog.GetPath()
#                self.text_ctrl_output.SetLabel(path)
#                print path
#            dialog.Destroy()
#            
    def onSpinYear(self, event):
        self.year = self.spin_year.GetValue()
        #update the groups based on the year
        pathForExportsheet = self.text_ctrl_export.GetValue()
        self.setGroups(pathForExportsheet)
        self.setTerms(pathForExportsheet)
        print self.year
    
    
    
    
    
    def onGenerate(self, event):
        #clear error stylings
        self.clearErrorStylings()
        
        
        while(True):
            #error checking
            problemChildren = []
            
            
            #year
            year = self.year

            #export_location
            export_location = self.text_ctrl_export.GetValue()
            if not( os.access(self.text_ctrl_export.GetValue(), os.F_OK)):
                problemChildren.append((self.text_ctrl_export, "You did not choose a valid export.xls file"))
                break

            
            #term
            checkterm = self.combo_term.GetValue()
            term = ""
            if checkterm == "":
                problemChildren.append((self.combo_term,"You did not select a term; if there are no groups available, make sure the year/export file are correct"))
                break
            else:
                termtuple = self.combo_term.GetClientData(self.combo_term.GetSelection())
                term = termtuple.term
                tt= termtuple.termTitle            
    
                
            #now check if there is a grade file in this same folder
            grades_location = export_location.replace("export.xls","")
            grades_location += ("report_sheets_"+str(year)+"_"+str(term)+".xls")
            if not( os.access(grades_location, os.F_OK)):
                problemChildren.append((self.text_ctrl_export, "You might need to move your files; there is no file report_sheets_"+str(year)+"_"+str(term)+".xls in the export folder"))
            
            #group
            group = self.combo_group.GetValue()
            if group == "":
                problemChildren.append((self.combo_group, "You did not select a group; if there are no groups available, make sure the year/export file are correct"))      
            
            #report Type
            for b in self.radio_buttons_report:
                if b.GetValue() == True:
                    repType = ReportType.reportTypesDic[b.GetLabel()]
                    print "Report type is: "
                    print repType
                    break;
            #average calculation type
            for b in self.radio_buttons_average:
                if b.GetValue() == True:
                    aveType = AverageType.aveTypesDic[b.GetLabel()]
                    print "Average type is: "
                    print aveType
                    break;
            
            
#            #htmlOutputDir
#            htmlOutputDir = self.text_ctrl_output.GetValue()
#            #print self.text_ctrl_output.GetValue()
#            if not( os.access(self.text_ctrl_output.GetValue(), os.F_OK)):
#                problemChildren.append((self.text_ctrl_output, "You did not select a good output folder; The output folder you selected doesn't exsist or you do not have the right permissions"))
#            
            htmlOutputDir = export_location.replace("export.xls","")
            htmlOutputDir += "GENERATED\\"
            print htmlOutputDir
            if not os.access(htmlOutputDir, os.F_OK):
                os.mkdir(htmlOutputDir)
            else:
                print "the generated directory already exsists"
            
            noerror = self.errorCheckAdvancedStuff(grades_location, term)
            
            if noerror != 0:
                problemChildren.append(noerror)
    
            break;
            #error check advanced stuff
    
        #additional error checking of the sheets, whether the export sheet is called export
        #maybe here check whether there is a grade sheet for the correct term in that directory
        
        #create userinputs

        if len(problemChildren) != 0:
            self.clearErrorStylings()
            self.setErrorStylings(problemChildren)
        else:
            uIs = UserInput(export_location = export_location,
                            year= year,
                            term = term,
                            tt = tt,
                            group = group,
                            repType = repType,
                            aveType = aveType,
                            htmlOutputDir = htmlOutputDir)
            #deal with advanced stuff
            self.setAdvancedStuff(uIs)
            print "MADE UI"
            
            
            #generate_report(uIs)
        
    def setErrorStylings(self,problemChildren):
        errorstring = "Could not generate because of the following errors:\n"
        print problemChildren
        for pc in problemChildren:
            message = pc[1]
            pc = pc[0]
            if isinstance(pc, wx.ComboBox):
                sizer = pc.GetContainingSizer()
                if sizer != None:
                    siblings = sizer.GetChildren()
                    for s in siblings:
                        s = s.GetWindow()
                        if isinstance(s, wx.StaticText) and s.GetLabel() == "Term" or s.GetLabel() == "Group":                            
                            s.SetLabel("*"+s.GetLabelText())
                        
                    print "it's a combobox"
            pc.SetBackgroundColour(wx.RED)
            errorstring += (message + "\n")
            
        if self.combo_term.IsEmpty() or self.combo_group.IsEmpty():
            self.text_year.SetLabel("*"+self.text_year.GetLabelText())
            errorstring += ("You might not have selected a good year; Please select a different year that has terms and groups \n")
        self.error_text.SetLabel(errorstring)
        
        self.Refresh()
    

        #clean everything up
        #set error stylings for all the problem children
    def clearErrorStylings(self):
        allitems = self.GetChildren()[0].GetChildren()
        mainpanelc = allitems[0].GetChildren()
        advancedpanelc = allitems[1].GetChildren()
        
        print mainpanelc
        print advancedpanelc
        for i in mainpanelc:
            i.SetBackgroundColour(wx.NullColour)
            curLabel = i.GetLabel()
            curLabel = curLabel.replace("*","")
            i.SetLabel(curLabel)
        for i in advancedpanelc:
            i.SetBackgroundColour(wx.NullColour)
            curLabel = i.GetLabel()
            curLabel = curLabel.replace("*","")
            i.SetLabel(curLabel)
        self.error_text.SetLabel(GradeGadgetFrame.PEACEFUL_MESSAGE)
                            
        #self.text_ctrl_export.SetBackgroundColour(wx.NullColour)
        #self.Refresh()
        #return
    def makeAdvancedRewriteHeadingBox(self, heading, advancedpanel, a_static_box_for_headings):
        a_heading_row = wx.BoxSizer(wx.HORIZONTAL)
        
        a_static_text = wx.StaticText(advancedpanel, -1, heading)
        a_text_control = wx.TextCtrl(advancedpanel, -1, "", name=(heading+ " Heading for Excel"))
        
        a_heading_row.Add(a_static_text,1,flag=wx.ALL, border=5)
        a_heading_row.Add(a_text_control,4,flag=wx.ALL|wx.EXPAND, border=5)
        
        a_static_box_for_headings.Add(a_heading_row,1,flag=wx.ALL|wx.EXPAND, border=5)

        return a_text_control

    def errorCheckAdvancedStuff(self,gradesfilepath,term):
        try:
            grades_workbook = open_workbook(gradesfilepath)
            gradesheet = grades_workbook.sheet_by_name(term)
            
        except (IOError, biffh.XLRDError):
            print "Can't open or get the file " + gradesfilepath
            return (self.text_ctrl_export, "Please choose a different export file; can't open it to check whether you advanced choices are OK")        

        for h in self.headings_list :
                if h.GetValue().strip() != "":
                    foundMatchingHeading = False
                    for col in range(gradesheet.ncols):
                        if gradesheet.cell(0,col).value==h.GetValue():
                            foundMatchingHeading = True
                            break
                    if not foundMatchingHeading:
                        return(h, "You types an incorrect heading. Please fix your heading(s) in the advanced tab. You can trying Copy Pasting from the Excel sheet")
        return 0            
                            
                    
        
        
    def setAdvancedStuff(self,ui):
        if (self.a_text_control_etm.GetValue().strip() != ""):
            ui.setETM(self.a_text_control_etm.GetValue())
        if (self.a_text_control_final.GetValue().strip() != ""):
            ui.setFINAL(self.a_text_control_final.GetValue())
        if (self.a_text_control_mtm.GetValue().strip() != ""):
            ui.setMTM(self.a_text_control_mtm.GetValue())
        if (self.a_text_control_comment.GetValue().strip() != ""):
            ui.setCOMMENT(self.a_text_control_comment.GetValue())
        if (self.a_text_control_template_location.GetValue().strip() != ""):
            ui.setTEMPLATES_FOLDER(self.a_text_control_template_location.GetValue())
        
        
app = wx.App(0) # 0 makes it go to standard output instead of the gui window
GradeGadgetFrame(None)
app.MainLoop()
#app = MyApp(redirect=True)
#app.MainLoop()