"""
This example demonstrates the proper use of project: lazgui
"""
import sys
import os

sys.path.insert(0, os.path.abspath("../../"))  # needed to find lazgui development version

from lazgui.laz_gui import LazarusGUI
from lazgui.form import Form
from lazgui.button import Button
from lazgui.labeled_edit import LabeledEdit
from lazgui.layout import Layout
from lazgui.layout import VStackPanel, HStackPanel, GridPanel


Lay = GridPanel( )
for i in [3,5,9]:
    for j in [2,6,8]:
        Lay.add_widget( Button(widget_name='Btn'), row=i, col=j )

Lay.add_widget( Button(widget_name='DoSompin_Wide', Width=100), row=5, col=6 )

Lay2 = HStackPanel()
Lay2.add_widget( Button(widget_name='XXX', Width=30) )
Lay2.add_widget( Button(widget_name='XXX', Width=30) )
Lay2.summ_print()
Lay.add_widget( Lay2, row=11, col=2 )

print '='*55
Lay.summ_print()
print '='*55

F = Form( form_name='MyForm1', layout=Lay,
          Left=611,  Height=240,  Top=162,  Width=320, 
          Caption=None,  LCLVersion='1.6.0.4')

C = LazarusGUI(project_name='ProjWhat', form1_obj=F)

C.save_project_files( path_name=r'D:\tmp\test_lazgui\v1', over_write_OK=True )
