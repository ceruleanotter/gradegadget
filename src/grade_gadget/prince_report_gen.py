'''
Created on Aug 31, 2012

@author: Lyla
'''
from xml.dom.minidom import parseString
from user_inputs import *
def generatePrinceReports(students):

    doc = parseString("""<html>
        <head>
            <script type="text/javascript">
                var a = 'I love &amp;aacute; letters'
            </script>
        </head>
        <body>
            <h1>And I like the fact that 3 &gt; 1</h1>
        </body>
        </html>""")

    
    
    with open("reports_for_"+group+"_term_"+term+"_"+year+".xhtml", "w") as f:
        f.write( doc.toxml() )
    
