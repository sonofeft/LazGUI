"""
This example demonstrates the proper use of project: lazgui
"""
import sys
import os

sys.path.insert(0, os.path.abspath("../../"))  # needed to find lazgui development version

from lazgui.laz_gui import LazarusGUI
from lazgui.form import Form
from lazgui.button import Button
from lazgui.edit import Edit
from lazgui.label import Label
from lazgui.labeled_edit import LabeledEdit
from lazgui.layout import Layout
from lazgui.layout import VStackPanel, HStackPanel, GridPanel


Lay = VStackPanel( )

Lay.add_widget( Label( widget_name='Get_Text', Caption='Label for Get_Text', BottomMargin=0) )
Lay.add_widget( Button(widget_name='Do Wide Things', Width=100, TopMargin=0) )

Lay.add_widget( Edit(widget_name='Get Stuff', label_text='Enter Stuff') )


Lay.summ_print()
print '='*55

F = Form( form_name='MyForm1', layout=Lay,
          Left=611,  Height=240,  Top=162,  Width=320, 
          Caption=None,  LCLVersion='1.6.0.4')

C = LazarusGUI(project_name='ProjWhat', form1_obj=F)

C.save_project_files( path_name=r'D:\tmp\test_lazgui\v1', over_write_OK=True )
