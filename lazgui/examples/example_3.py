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
from lazgui.labeled_edit import LabeledEdit
from lazgui.layout import Layout
from lazgui.layout import VStackPanel, HStackPanel, GridPanel


Lay = GridPanel( )
Lay.add_widget( Button(widget_name='On Top', Width=100), row=0, col=0 )
for j in xrange(3):
    Lay.add_widget( LabeledEdit(label_text='Enter #%i'%j + j*'abc'), 
                    row=1, col=j)

Lay.add_widget( Edit(widget_name='At Bottom', Width=100), row=2, col=2 )

Lay.summ_print()
print '='*55

F = Form( form_name='MyForm1', layout=Lay,
          Left=611,  Height=240,  Top=162,  Width=320, 
          Caption=None,  LCLVersion='1.6.0.4')

C = LazarusGUI(project_name='ProjWhat', form1_obj=F)

C.save_project_files( path_name=r'D:\tmp\test_lazgui\v1', over_write_OK=True )
