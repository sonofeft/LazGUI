"""
This example demonstrates the proper use of project: lazgui
"""
import sys
import os

sys.path.insert(0, os.path.abspath("../../"))  # needed to find lazgui development version

from lazgui.gui_factory import *

Lay = get_layout(layout_type='vstack', Left=41,  Height=0,  Top=42,  Width=0, 
                 TopMargin=6, RightMargin=6, BottomMargin=6, LeftMargin=6)

Lay.add_widget( get_label( widget_name='Get_Text', Caption='Label for Get_Text', BottomMargin=0) )
Lay.add_widget( get_button(widget_name='Do Wide Things', Width=100, TopMargin=0) )

Lay.add_widget( get_edit(widget_name='Get What', label_text='', initial_value='No Label') )

Lay.add_widget( get_edit(widget_name='Get Stuff', 
                         label_text='Enter Stuff', initial_value='Has Label') )
Lay.add_widget( get_edit(widget_name='Get Other Stuff', 
                         label_text='Enter Other Stuff', initial_value='LabeledEdit') )

Lay.add_widget( get_edit(edit_type='other', widget_name='GetValue',  
                initial_value='VLayout Wrapped', label_text='xxx') )


Lay.summ_print()
print '='*55

F = get_form( form_name='MyForm1', layout=Lay,
          Left=611,  Height=240,  Top=162,  Width=320, 
          Caption=None,  LCLVersion='1.6.0.4')

C = get_gui(project_name='ProjWhat', form1_obj=F)

C.save_project_files( path_name=r'D:\tmp\test_lazgui\v1', over_write_OK=True )
