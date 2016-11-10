"""
Wraps the Lazarus *.lps file that defines the project session.
Holds project_name, unit names, etc.
"""
import sys
from copy import deepcopy
import xml.etree.ElementTree as ET

class LPS_File( object ):
    
    def __init__(self, project_name='project1', form1_name='Form1'):
        
        self.project_name = str(project_name)
        self.lpr_name = self.project_name + '.lpr'
        
        self.xml_root = ET.XML( LPS_TEMPLATE_STR )
        
        self.ProjectSession = self.xml_root.find('ProjectSession')
        
        self.Units = self.ProjectSession.find('Units')
        self.unitL = [c for c in self.Units]
        
        self.form_name_set = set( [form1_name.lower()] ) # save set of form names in lower case
        
        self.unitL[0].find('Filename').set('Value', self.lpr_name )
        
        unit1_name = form1_name + '_Unit'
        
        self.unitL[1].find('Filename').set('Value', unit1_name.lower() + '.pas')
        self.unitL[1].find('UnitName').set('Value', unit1_name )
        self.unitL[1].find('ComponentName').set('Value', form1_name )
        
                
    def add_form(self, new_form_name=None):
        
        
        if new_form_name is None:
            print "Need a valid new_form_name in lpi_wrapper"
            sys.exit()
            
        if new_form_name.lower() in self.form_name_set:
            print "Duplicate form names are NOT allowed in lpi_wrapper"
            sys.exit()
            
        self.form_name_set.add( new_form_name.lower() )
            
        unit_node = deepcopy( self.unitL[-1] )
        #unit_node = self.unitL[-1].copy()
        
        unit_node.tag = 'Unit%i'%len(self.unitL)
        
        #unit_node = ET.SubElement(self.Units, 'Unit%i'%len(self.unitL), self.unitL[-1].attrib)
        
        unit_name = new_form_name + '_Unit'
        
        unit_node.find('Filename').set('Value', unit_name.lower() + '.pas')
        unit_node.find('UnitName').set('Value', unit_name )
        unit_node.find('ComponentName').set('Value', new_form_name )
        
        self.unitL.append( unit_node )
        self.Units.append( unit_node )
        
        self.Units.set('Count', str(len(self.unitL)) )
        
    
    def file_contents(self):
        self.Units.set('Count', str(len(self.unitL)) )
        
        return """<?xml version="1.0" encoding="UTF-8"?>\n""" + ET.tostring( self.xml_root )
    
    def summ_print(self):
        print 'xml_root =',self.xml_root
        print 'ProjectSession =',self.ProjectSession
        print 'Units =',self.Units
        for c in self.unitL:
            print '    Unit =',c
        

LPS_TEMPLATE_STR = """<?xml version="1.0" encoding="UTF-8"?>
<CONFIG>
  <ProjectSession>
    <PathDelim Value="\"/>
    <Version Value="9"/>
    <BuildModes Active="Default"/>
    <Units Count="2">
      <Unit0>
        <Filename Value="project1.lpr"/>
        <IsPartOfProject Value="True"/>
        <EditorIndex Value="-1"/>
        <WindowIndex Value="-1"/>
        <TopLine Value="-1"/>
        <CursorPos X="-1" Y="-1"/>
        <UsageCount Value="20"/>
      </Unit0>
      <Unit1>
        <Filename Value="unit1.pas"/>
        <IsPartOfProject Value="True"/>
        <ComponentName Value="Form1"/>
        <ResourceBaseClass Value="Form"/>
        <UnitName Value="Unit1"/>
        <IsVisibleTab Value="True"/>
        <UsageCount Value="20"/>
        <Loaded Value="True"/>
        <LoadedDesigner Value="True"/>
      </Unit1>
    </Units>
    <JumpHistory HistoryIndex="-1"/>
  </ProjectSession>
</CONFIG>
"""

if __name__ == "__main__":
    
    LPS = LPS_File(project_name='ChkProject', form1_name='ChkForm')
    LPS.add_form(new_form_name='ZZZForm')
    LPS.add_form(new_form_name='ZZZForm')
    
    LPS.summ_print()
    print '-'*55
    #print LPS.file_contents()
    
    ET.dump( LPS.xml_root )
    