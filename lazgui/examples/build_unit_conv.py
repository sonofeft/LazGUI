"""
This example demonstrates the proper use of project: lazgui
"""
import sys
import os

here = os.path.abspath(os.path.dirname(__file__))

from lazgui.gui_factory import *

ItemL = ['First Choice','Second Pick','Third One','Last One']

Lay = get_layout(layout_type='vstack', Left=10,  Height=0,  Top=10,  Width=0, 
                 TopMargin=0, RightMargin=0, BottomMargin=0, LeftMargin=0)

HLay1 = get_layout(layout_type='hstack', Left=0,  Height=0,  Top=0,  Width=0, 
                 TopMargin=0, RightMargin=0, BottomMargin=0, LeftMargin=0)
HLay1.add_widget(get_combobox(Items=ItemL, ItemIndex=1, ItemHeight=15,
                 widget_name='Category', Left=0,  Height=10,  Top=0,  Width=20, 
                 TopMargin=0, RightMargin=0, BottomMargin=0, LeftMargin=0,
                 has_OnClick=False, has_OnSelect=True))
HLay1.add_widget( get_label( widget_name='Category', Caption='Label for Get_Text', 
                           BottomMargin=0) )

HLay2 = get_layout(layout_type='hstack', Left=0,  Height=0,  Top=0,  Width=0, 
                 TopMargin=0, RightMargin=0, BottomMargin=0, LeftMargin=0)
HLay2.add_widget(get_combobox(Items=ItemL, ItemIndex=1, ItemHeight=15,
                 widget_name='Units', Left=0,  Height=10,  Top=0,  Width=20, 
                 TopMargin=0, RightMargin=0, BottomMargin=0, LeftMargin=0,
                 has_OnClick=False, has_OnSelect=True))
HLay2.add_widget( get_label( widget_name='Units', Caption='Label for Get_Text', 
                           BottomMargin=0) )


HLay3 = get_layout(layout_type='hstack', Left=0,  Height=0,  Top=0,  Width=0, 
                 TopMargin=0, RightMargin=0, BottomMargin=0, LeftMargin=0)
HLay3.add_widget(get_edit(widget_name='Value', label_text='', initial_value='1.0'))
HLay3.add_widget( get_label( widget_name='Value', Caption='Value', 
                           BottomMargin=0) )

Lay.add_widget( HLay1 )
Lay.add_widget( HLay2 )
Lay.add_widget( HLay3 )


Lay.summ_print()
print '='*55

F = get_form( form_name='MyForm1', layout=Lay, has_file_menu=False,
          Left=611,  Height=240,  Top=162,  Width=320, 
          Caption=None,  LCLVersion='1.6.0.4')


C = LazarusGUI(project_name='ProjWhat', form1_obj=F)

C.save_project_files( path_name=r'D:\tmp\test_lazgui\v1', over_write_OK=True )
