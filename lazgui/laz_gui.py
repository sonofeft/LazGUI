#!/usr/bin/env python
# -*- coding: ascii -*-

r"""
LazGUI helps to create Lazarus Pascal GUI project.

LazGUI will place all of the required files for the Lazarus project
into a subdirectory by project name.  The project can be built using "lazbuild"
that comes with a Lazarus install, or by opening the <project_name>.lpi file with
the Lazarus IDE.


LazGUI
Copyright (C) 2016  Charlie Taylor

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

-----------------------

"""
import os, sys
import shutil
here = os.path.abspath(os.path.dirname(__file__))
ref_proj_files = os.path.join( here, 'ref_proj_files' )
#print 'ref_proj_files =',ref_proj_files

from lpi_wrapper import LPI_File
from lps_wrapper import LPS_File
from lpr_wrapper import LPR_File

# for multi-file projects see LICENSE file for authorship info
# for single file projects, insert following information
__author__ = 'Charlie Taylor'
__copyright__ = 'Copyright (c) 2016 Charlie Taylor'
__license__ = 'GPL-3'
exec( open(os.path.join( here,'_version.py' )).read() )  # creates local __version__ variable
__email__ = "cet@appliedpython.com"
__status__ = "3 - Alpha" # "3 - Alpha", "4 - Beta", "5 - Production/Stable"

#
# import statements here. (built-in first, then 3rd party, then yours)
#
# Code goes below.
# Adjust docstrings to suite your taste/requirements.
#

class LazarusGUI(object):
    """LazGUI helps to create Lazarus Pascal GUI project."""

    def __init__(self, project_name='project1', form1_obj=None, data_file_ext='proj_dat'):
        """Inits LazarusGUI"""
        self.project_name = str(project_name)
        self.data_file_ext= data_file_ext

        self.form_name_set = set() # save set of form names in lower case
        self.formL = []
        
        if form1_obj is not None:
            self.add_form( form1_obj )
    
    def add_form(self, form_obj):
        
        form_name = form_obj.form_name 
        form_obj.set_laz_gui_obj( self )
        
        #  Don't allow duplicate form names
        while form_name.lower() in self.form_name_set:
            form_name = form_name + str( (len(self.formL) + 1) )
        self.form_name_set.add( form_name.lower() )
        
        self.formL.append( form_obj )
        
    def save_project_files(self, path_name='', over_write_OK=False):
        if len(self.formL)==0:
            print 'Can NOT create project... No Forms have been added.'
            return
            
        targ_abs_path = os.path.abspath( path_name )
        
        if os.path.isfile( targ_abs_path ):
            print 'Can NOT create project... The provided path_name is an existing file.'
            print 'Need to provide a directory name.'
            print 'Existing file =',targ_abs_path
            return

        if os.path.isdir( targ_abs_path ):
            if over_write_OK:
                print 'Using existing directory for Lazarus project.'
                print 'path_name =',targ_abs_path
            else:
                print 'Can NOT create project... The provided directory already exists.'
                print 'Enter a new directory name OR set parameter "over_write_OK=True".'
                print 'Existing directory =',targ_abs_path
                return
        else:            
            os.mkdir( targ_abs_path )
            print "created new Lazarus project directory:",targ_abs_path
        
        form1 = self.formL[0]
        
        lpi_obj = LPI_File( project_name=self.project_name, form1_name=form1.form_name )
        lps_obj = LPS_File( project_name=self.project_name, form1_name=form1.form_name )
        lpr_obj = LPR_File( project_name=self.project_name, form1_name=form1.form_name )
        
        for f in self.formL[1:]:
            lpi_obj.add_form( new_form_name=f.form_name )
            lps_obj.add_form( new_form_name=f.form_name )
            lpr_obj.add_form( new_form_name=f.form_name )
        
        #  copy              I/O Variable Get/Set,    and required menu History files
        for copy_fname in ['get_set_io_var.pas', 'HistoryFiles.pas', 'HistoryLazarus.lrs']:
            src_fname = os.path.join( ref_proj_files, copy_fname )
            targ_fname = os.path.join( targ_abs_path, copy_fname )
            print 'Copying',src_fname,' --> ',targ_fname
            shutil.copy(src_fname, targ_fname)
        
        # Create  Resource File
        src_fname = os.path.join( ref_proj_files, 'project1.res' )
        targ_fname = os.path.join( targ_abs_path, '%s.res'%self.project_name )
        print 'Copying',src_fname,' --> ',targ_fname
        shutil.copy(src_fname, targ_fname)
        
        # Create  Icon
        src_fname = os.path.join( ref_proj_files, 'project1.ico' )
        targ_fname = os.path.join( targ_abs_path, '%s.ico'%self.project_name )
        print 'Copying',src_fname,' --> ',targ_fname
        shutil.copy(src_fname, targ_fname)
        
        # Create *.lpi file (i.e. ProjectOptions, Units, CompilerOptions, Debugging)
        targ_fname = os.path.join( targ_abs_path, '%s.lpi'%self.project_name )
        print 'Saving --> ',targ_fname
        with open(targ_fname, 'w') as f:
            f.write( lpi_obj.file_contents() )
        
        # Create *.lps file (i.e. ProjectSession, Units, PathDelim)
        targ_fname = os.path.join( targ_abs_path, '%s.lps'%self.project_name )
        print 'Saving --> ',targ_fname
        with open(targ_fname, 'w') as f:
            f.write( lps_obj.file_contents() )
        
        # Create *.lpr file (i.e. Pascal source for overall project)
        targ_fname = os.path.join( targ_abs_path, '%s.lpr'%self.project_name )
        print 'Saving --> ',targ_fname
        with open(targ_fname, 'w') as f:
            f.write( lpr_obj.file_contents() )
        
        # Create *.pas and *.lfm for each of the Form units
        for form in self.formL:
            targ_fname = os.path.join( targ_abs_path, '%s.pas'%form.unit_name.lower() )
            print 'Saving --> ',targ_fname
            with open(targ_fname, 'w') as f:
                f.write( form.pas_file_contents() )
            
            targ_fname = os.path.join( targ_abs_path, '%s.lfm'%form.unit_name.lower() )
            print 'Saving --> ',targ_fname
            with open(targ_fname, 'w') as f:
                f.write( form.lfm_file_contents() )
                
        # Create *.bat file to compile and run project
        targ_fname = os.path.join( targ_abs_path, '%s.bat'%self.project_name )
        print 'Saving --> ',targ_fname
        with open(targ_fname, 'w') as f:
            f.write( BAT_FILE_TEMPLATE.format( **self.__dict__ ) )
        
BAT_FILE_TEMPLATE = """rem delete any existing EXE file
del {project_name}.exe
lazbuild {project_name}.lpi

rem Now try to run the EXE file
{project_name}.exe
"""

if __name__ == '__main__':
    from form import Form
    from button import Button
    from labeled_edit import LabeledEdit
    from layout import Layout
    from layout import VStackPanel, HStackPanel
    
    Lay = VStackPanel(Left=10,  Height=0,  Top=10,  Width=0, 
                          TopMargin=10, RightMargin=10, BottomMargin=10, LeftMargin=10)
    

    for i in xrange(3):
        B = Lay.add_widget( Button( widget_name='DoSompin_%i'%i, Left=41+i*5,  Height=25,  
                                    Top=42+i*5,  Width=75+i*5, 
                                    Caption=None, has_OnClick=True) )
                    
        print '#%i) bbox ='%i, B.BBox
    
    Lay.add_widget(LabeledEdit( label_text='Enter Diameter', widget_name='GetDiam', 
                   initial_value='4.56789012345678905678901234567890',   
                   Left=1,  Height=23,  Top=1,  Width=80, 
                   Caption='Enter Diameter', has_OnClick=True) )

    F = Form( form_name='MyForm1', layout=Lay,
              Left=611,  Height=240,  Top=162,  Width=320, 
              Caption=None,  LCLVersion='1.6.0.4')

    C = LazarusGUI(project_name='ProjWhat', form1_obj=F)
    
    C.save_project_files( path_name=r'D:\tmp\test_lazgui\v1', over_write_OK=True )
