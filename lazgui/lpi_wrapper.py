"""
Wraps the Lazarus *.lpi file that defines the project.
Holds project_name, unit names, etc.
"""
import sys
from copy import deepcopy
import xml.etree.ElementTree as ET

class LPI_File( object ):
    
    def __init__(self, project_name='project1', form1_name='Form1'):
        
        self.project_name = str(project_name)
        self.lpr_name = self.project_name + '.lpr'
        
        self.xml_root = ET.XML( LPI_TEMPLATE_STR )
        
        self.ProjectOptions = self.xml_root.find('ProjectOptions')
        self.General = self.ProjectOptions.find('General')
        self.Title = self.General.find('Title')
        self.Title.set('Value', self.project_name)
        
        self.Units = self.ProjectOptions.find('Units')
        self.unitL = [c for c in self.Units]
        
        self.form_name_set = set( [form1_name.lower()] ) # save set of form names in lower case
        
        self.unitL[0].find('Filename').set('Value', self.lpr_name )
        
        unit1_name = form1_name + '_Unit'
        
        self.unitL[1].find('Filename').set('Value', unit1_name.lower() + '.pas')
        self.unitL[1].find('UnitName').set('Value', unit1_name )
        self.unitL[1].find('ComponentName').set('Value', form1_name )
        
        
        self.CompilerOptions = self.xml_root.find('CompilerOptions')
        self.Target = self.CompilerOptions.find('Target')
        self.Target.find('Filename').set('Value', self.project_name)
        
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
        print 'General =',self.General
        print 'Title =',self.Title
        print 'ProjectOptions =',self.ProjectOptions
        print 'Units =',self.Units
        for c in self.unitL:
            print '    Unit =',c
        

LPI_TEMPLATE_STR = """<?xml version="1.0" encoding="UTF-8"?>
<CONFIG>
  <ProjectOptions>
    <Version Value="9"/>
    <PathDelim Value="\"/>
    <General>
      <SessionStorage Value="InProjectDir"/>
      <MainUnit Value="0"/>
      <Title Value="project1"/>
      <ResourceType Value="res"/>
      <UseXPManifest Value="True"/>
      <Icon Value="0"/>
    </General>
    <i18n>
      <EnableI18N LFM="False"/>
    </i18n>
    <VersionInfo>
      <StringTable ProductVersion=""/>
    </VersionInfo>
    <BuildModes Count="1">
      <Item1 Name="Default" Default="True"/>
    </BuildModes>
    <PublishOptions>
      <Version Value="2"/>
    </PublishOptions>
    <RunParams>
      <local>
        <FormatVersion Value="1"/>
      </local>
    </RunParams>
    <RequiredPackages Count="1">
      <Item1>
        <PackageName Value="LCL"/>
      </Item1>
    </RequiredPackages>
    <Units Count="2">
      <Unit0>
        <Filename Value="project1.lpr"/>
        <IsPartOfProject Value="True"/>
      </Unit0>
      <Unit1>
        <Filename Value="unit1.pas"/>
        <IsPartOfProject Value="True"/>
        <ComponentName Value="Form1"/>
        <ResourceBaseClass Value="Form"/>
        <UnitName Value="Unit1"/>
      </Unit1>
    </Units>
  </ProjectOptions>
  <CompilerOptions>
    <Version Value="11"/>
    <PathDelim Value="\"/>
    <Target>
      <Filename Value="project1"/>
    </Target>
    <SearchPaths>
      <IncludeFiles Value="$(ProjOutDir)"/>
      <UnitOutputDirectory Value="lib\$(TargetCPU)-$(TargetOS)"/>
    </SearchPaths>
    <Linking>
      <Options>
        <Win32>
          <GraphicApplication Value="True"/>
        </Win32>
      </Options>
    </Linking>
  </CompilerOptions>
  <Debugging>
    <Exceptions Count="3">
      <Item1>
        <Name Value="EAbort"/>
      </Item1>
      <Item2>
        <Name Value="ECodetoolError"/>
      </Item2>
      <Item3>
        <Name Value="EFOpenError"/>
      </Item3>
    </Exceptions>
  </Debugging>
</CONFIG>
"""

if __name__ == "__main__":
    
    LPI = LPI_File(project_name='ChkProject', form1_name='ChkForm')
    LPI.add_form(new_form_name='ZZZForm')
    LPI.add_form(new_form_name='ZZZForm')
    
    LPI.summ_print()
    print '-'*55
    #print LPI.file_contents()
    
    ET.dump( LPI.xml_root )
    