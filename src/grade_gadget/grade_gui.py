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
from xlrd import open_workbook,empty_cell
from grade_gadget import generate_report

class GradeGadgetFrame(wx.Frame):
    """
    This is GradeGadgetFrame.  It contains everything for the grade gadget gui.
    """
    
    def __init__(self, *args, **kwargs):
        super(GradeGadgetFrame, self).__init__(*args, **kwargs) 
            
        self.InitUI()
        
    def InitUI(self):
        self.currentDirectory = os.getcwd()
        self.SetSize((500, 350))
        self.SetTitle('Gashora Grade Gadget -- Report Generator')
        
        
        mainpanel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)
        row1 = wx.BoxSizer(wx.HORIZONTAL)
        row2 = wx.BoxSizer(wx.HORIZONTAL)
        row3 = wx.BoxSizer(wx.HORIZONTAL)        
        row4 = wx.BoxSizer(wx.HORIZONTAL)    
        row5 = wx.BoxSizer(wx.HORIZONTAL)    
        row6 = wx.BoxSizer(wx.HORIZONTAL)    
        row7 = wx.BoxSizer(wx.HORIZONTAL)
        row8 = wx.BoxSizer(wx.HORIZONTAL)
        row9 = wx.BoxSizer(wx.HORIZONTAL)
        
        #row1                   
        box_chooseExport = wx.StaticBox(mainpanel, label='Choose School Export File');
        sb_chooseExport = wx.StaticBoxSizer(box_chooseExport, wx.HORIZONTAL)
        
        self.text_ctrl_export = wx.TextCtrl(mainpanel, -1, "click browse", style=wx.TE_READONLY)
        button_browse_export = wx.Button(mainpanel, label="Browse")
        
        sb_chooseExport.Add(self.text_ctrl_export,1,flag=wx.ALL|wx.EXPAND, border=5)
        sb_chooseExport.Add(button_browse_export,flag=wx.ALL, border=5)        
        
        row1.Add(sb_chooseExport,1, flag=wx.ALL|wx.EXPAND, border=5)
        
        
        #row2
        text_term = wx.StaticText(mainpanel, label='Term');
        self.combo_term = wx.ComboBox(mainpanel, choices=[],style=wx.CB_READONLY)
        row2.Add(text_term,flag=wx.ALL|wx.EXPAND, border=5)
        row2.Add(self.combo_term,flag=wx.ALL|wx.EXPAND, border=5)
        
        text_year = wx.StaticText(mainpanel, label='Year');
        self.year = str(datetime.datetime.now().year)
        print self.year #!need to add change year functionality
        self.spin_year = wx.SpinCtrl(mainpanel, value=self.year)                
        self.spin_year.SetRange(2010,2500)
        row2.Add(text_year,flag=wx.ALL|wx.EXPAND, border=5)        
        row2.Add(self.spin_year,flag=wx.ALL|wx.EXPAND, border=5)  
                
        #row3
        text_group = wx.StaticText(mainpanel, label='Group');
        self.combo_group = wx.ComboBox(mainpanel, choices=[], style=wx.CB_READONLY)
        row3.Add(text_group,flag=wx.ALL|wx.EXPAND, border=5)  
        row3.Add(self.combo_group,flag=wx.ALL|wx.EXPAND, border=5)  
                
        #row4
        text_type = wx.StaticText(mainpanel, label='Type of Report');
        combo_type = wx.ComboBox(mainpanel, choices=['Midterm','Final','GPAs'], style=wx.CB_READONLY)
        row4.Add(text_type,flag=wx.ALL|wx.EXPAND, border=5)  
        row4.Add(combo_type,flag=wx.ALL|wx.EXPAND, border=5)  
        
        
        #row5
        text_ave = wx.StaticText(mainpanel, label='Average Calculation Style');
        rb_course = wx.RadioButton(mainpanel, label='Course', style=wx.RB_GROUP)
        rb_section = wx.RadioButton(mainpanel, label='Section')
        row5.Add(text_ave,flag=wx.ALL|wx.EXPAND, border=5)  
        row5.Add(rb_course,flag=wx.ALL|wx.EXPAND, border=5)  
        row5.Add(rb_section,flag=wx.ALL|wx.EXPAND, border=5)  
        
        #row6                   
        box_output = wx.StaticBox(mainpanel, label='Output Folder');
        sb_output = wx.StaticBoxSizer(box_output, wx.HORIZONTAL)
        
        self.text_ctrl_output = wx.TextCtrl(mainpanel, -1, "click browse", style=wx.TE_READONLY )
        button_browse_output = wx.Button(mainpanel, label="Browse")
        
        sb_output.Add(self.text_ctrl_output,1,flag=wx.ALL,border=5)
        sb_output.Add(button_browse_output,flag=wx.ALL,border=5)
        
        row6.Add(sb_output,1, flag=wx.ALL|wx.EXPAND, border=5)
        
        
        #line
        line = wx.StaticLine(mainpanel)
        
        #row7
        button_generate = wx.Button(mainpanel, label="Generate Report")
        row7.Add(button_generate,flag=wx.BOTTOM|wx.TOP, border=5)        
        
        vbox.Add(row1, flag=wx.EXPAND)
        vbox.Add(row2, flag=wx.EXPAND)
        vbox.Add(row3, flag=wx.EXPAND)
        vbox.Add(row4, flag=wx.EXPAND)
        vbox.Add(row5, flag=wx.EXPAND)        
        vbox.Add(row6, flag=wx.EXPAND)
    
        vbox.Add(line, flag=wx.EXPAND|wx.BOTTOM, border=10)
        
        vbox.Add(row7, flag=wx.ALIGN_CENTER)        
        
        mainpanel.SetSizer(vbox)
        
        #Event Stuff
        button_browse_export.Bind(wx.EVT_BUTTON, self.onBrowseExport)
        button_browse_output.Bind(wx.EVT_BUTTON, self.onBrowseOutputFolder)        
        self.spin_year.Bind(wx.EVT_SPIN, self.onSpinYear)
        
        
        
        
        
        
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
            self.combo_group.Clear()
            self.combo_group.AppendItems(groupsList)
            print groupsList
        except IOError:
            print "Can't open the file to find the groups"
                
    def setTerms(self, exportfilepath):
        try:
            school_workbook = open_workbook(exportfilepath)
            termsheet = school_workbook.sheet_by_name("Terms")
            termList = []
            for row in range(termsheet.nrows):
                if termsheet.cell(row,0).value==str(self.year):
                    termList.append(termsheet.cell(row,1).value)
            self.combo_term.Clear()
            self.combo_term.AppendItems(termList)
            print termList
        except IOError:
            print "Can't open the file to find the groups"
                   



    def onBrowseOutputFolder(self, event):
            print "output pressed"
            dialog = wx.DirDialog(self,
                                   message="Choose a directory",
                                   style=wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST| wx.DD_CHANGE_DIR,
                                   defaultPath=self.currentDirectory
                                   )
            
            if dialog.ShowModal() == wx.ID_OK:
                path = dialog.GetPath()
                self.text_ctrl_output.SetLabel(path)
                print path
            dialog.Destroy()
            
    def onSpinYear(self, event):
        self.year = self.spin_year.GetValue()
        #update the groups based on the year
        pathForExportsheet = self.text_ctrl_export.GetValue()
        self.setGroups(pathForExportsheet)
        print self.year
    

        
#
#        # Create the menubar
#        #menuBar = wx.MenuBar()
#
#        # and a menu 
#        #menu = wx.Menu()
#
#        # add an item to the menu, using \tKeyName automatically
#        # creates an accelerator, the third param is some help text
#        # that will show up in the statusbar
#        #menu.Append(wx.ID_EXIT, "E&xit\tAlt-X", "Exit this simple sample")
#
#        # bind the menu event to an event handler
#        #self.Bind(wx.EVT_MENU, self.OnTimeToClose, id=wx.ID_EXIT)
#
#        # and put the menu on the menubar
#        #menuBar.Append(menu, "&File")
#        #self.SetMenuBar(menuBar)
#
#        #self.CreateStatusBar()
#        
#
#        # Now create the Panel to put the other controls on.
#        panel = wx.Panel(self)
#
#        # and a few controls
#        #text = wx.StaticText(panel, -1, "Hello World!")
#        #text.SetFont(wx.Font(14, wx.SWISS, wx.NORMAL, wx.BOLD))
#        #text.SetSize(text.GetBestSize())
#        #btn = wx.Button(panel, -1, "Close")
#        #funbtn = wx.Button(panel, -1, "Just for fun...")
#        generateButton = wx.Button(panel, -1, "Click to Generate Report")
#        exportChoose = wx.Button(panel, -1, "Choose Export")
#        chooseExportText = wx.Window(panel, -1)
#        chooseExportText.text = "Hello World"
#
#
#
#        # bind the button events to handlers
#        self.Bind(wx.EVT_BUTTON, self.GenerateReport, generateButton)
#        self.Bind(wx.EVT_BUTTON, self.ExportLocation, exportChoose)
#    
#        #self.Bind(wx.EVT_BUTTON, self.OnTimeToClose, btn)
#        #self.Bind(wx.EVT_BUTTON, self.OnFunButton, funbtn)
#
#        # Use a sizer to layout the controls, stacked vertically and with
#        # a 10 pixel border around each
#        #sizer = wx.BoxSizer(wx.VERTICAL)
#        sizer = wx.FlexGridSizer(11,1,10,10)
#        #sizer.Add(text, 0, wx.ALL, 10)
#        #sizer.Add(btn, 0, wx.ALL, 10)
#        #sizer.Add(funbtn, 0, wx.ALL, 10)
#        sizer.Add(generateButton,0,wx.EXPAND)
#        sizer.Add(exportChoose, 0,wx.EXPAND)
#
#        
#        panel.SetSizer(sizer)
#        panel.Layout()
#
#
#    def GenerateReport (self, evt):
#        print "Generating report"
#        generate_report()
#
#    def OnTimeToClose(self, evt):
#        """Event handler for the button click."""
#        print "See ya later!"
#        self.Close()
#
#    def OnFunButton(self, evt):
#        """Event handler for the button click."""
#        print "Having fun yet?"
#        
#    def ExportLocation (self, evt):
#        print "fun"
#        print "CWD: %s\n" % os.getcwd()
#        # Create the dialog. In this case the current directory is forced as the starting
#        # directory for the dialog, and no default file name is forced. This can easilly
#        # be changed in your program. This is an 'open' dialog, and allows multitple
#        # file selections as well.
#        #
#        # Finally, if the directory is changed in the process of getting files, this
#        # dialog is set up to change the current working directory to the path chosen.
#        dlg = wx.FileDialog(
#            self, message="Choose a file",
#            defaultDir=os.getcwd(), 
#            defaultFile="",
#            wildcard=wildcard,
#            style=wx.OPEN | wx.MULTIPLE | wx.CHANGE_DIR
#            )
#
#        # Show the dialog and retrieve the user response. If it is the OK response, 
#        # process the data.
#        if dlg.ShowModal() == wx.ID_OK:
#            # This returns a Python list of files that were selected.
#            path = dlg.GetPath()
#
#            print 'You selected %d files:' % len(path)
#            print '           %s\n' % path
#
#        # Compare this with the debug above; did we change working dirs?
#        print "CWD: %s\n" % os.getcwd()
#
#        # Destroy the dialog. Don't do this until you are done with it!
#        # BAD things can happen otherwise!
#        dlg.Destroy()


#class GradeGadgetApp(wx.App):
#    def OnInit(self):
#        frame = GradeGadgetFrame(None, "Gashora Grade Gadget -- Report Generator")
#        self.SetTopWindow(frame)
#
#        print "Print statements go to this stdout window by default."
#
#        frame.Show(True)
#        return True

app = wx.App(0) # 0 makes it go to standard output instead of the gui window
GradeGadgetFrame(None)
app.MainLoop()
#app = MyApp(redirect=True)
#app.MainLoop()