import unittest
# import unittest2 as unittest # for versions of python < 2.7

"""
        Method                  Checks that
self.assertEqual(a, b)           a == b   
self.assertNotEqual(a, b)        a != b   
self.assertTrue(x)               bool(x) is True  
self.assertFalse(x)              bool(x) is False     
self.assertIs(a, b)              a is b
self.assertIsNot(a, b)           a is not b
self.assertIsNone(x)             x is None 
self.assertIsNotNone(x)          x is not None 
self.assertIn(a, b)              a in b
self.assertNotIn(a, b)           a not in b
self.assertIsInstance(a, b)      isinstance(a, b)  
self.assertNotIsInstance(a, b)   not isinstance(a, b)  

See:
      https://docs.python.org/2/library/unittest.html
         or
      https://docs.python.org/dev/library/unittest.html
for more assert options
"""

import sys, os

here = os.path.abspath(os.path.dirname(__file__)) # Needed for py.test
up_one = os.path.split( here )[0]  # Needed to find lazgui development version
if here not in sys.path[:2]:
    sys.path.insert(0, here)
if up_one not in sys.path[:2]:
    sys.path.insert(0, up_one)

from lazgui.laz_gui import LazarusGUI
from lazgui.gui_factory import *

class MyTest(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)
        self.myclass = LazarusGUI()

    def tearDown(self):
        unittest.TestCase.tearDown(self)
        del( self.myclass )

    def test_myclass_existence(self):
        """Check that myclass exists"""
        result = self.myclass

        # See if the self.myclass object exists
        self.assertTrue(result)
        
    def test_Panel(self):
        Lay = get_layout(layout_type='vstack', Left=0,  Height=20,  Top=0,  Width=20, 
                         TopMargin=6, RightMargin=6, BottomMargin=6, LeftMargin=6)

        Lay.add_widget( get_label( widget_name='Get_Text', Caption='Label for Get_Text', BottomMargin=0) )
        Lay.add_widget( get_button(widget_name='Do Wide Things', Width=100, TopMargin=0) )

        # =========== Panel

        LayPanel = get_layout(layout_type='vstack', Left=0,  Height=20,  Top=0,  Width=20, 
                         TopMargin=6, RightMargin=6, BottomMargin=6, LeftMargin=6)
        LayPanel.add_widget( get_edit(widget_name='Get What', label_text='', initial_value='No Label') )

        LayPanel.add_widget( get_edit(widget_name='Get Stuff', 
                                 label_text='Enter Stuff', initial_value='Has Label') )
        Lay.add_widget( get_panel(layout=LayPanel) )
        # ===================

        Lay.add_widget( get_edit(edit_type='other', widget_name='GetValue',  
                        initial_value='VLayout Wrapped', label_text='xxx') )
        Lay.add_widget( get_edit(widget_name='Get Other Stuff', 
                                 label_text='Enter Other Stuff', initial_value='LabeledEdit') )


        Lay.summ_print()
        print '='*55

        F = get_form( form_name='MyForm1', layout=Lay,
                  Left=800,  Height=240,  Top=10,  Width=320, 
                  Caption=None,  LCLVersion='1.6.0.4')

        C = get_gui(project_name='ProjWhat', form1_obj=F)
        
    def test_pagecontrol(self):

        Lay = get_layout(layout_type='vstack', Left=0,  Height=20,  Top=0,  Width=20, 
                         TopMargin=6, RightMargin=6, BottomMargin=6, LeftMargin=6)

        Lay.add_widget( get_label( widget_name='Get_Text', Caption='Label for Get_Text', BottomMargin=0) )
        Lay.add_widget( get_button(widget_name='Do Wide Things', Width=100, TopMargin=0) )

        # =========== PageControl

        Page = get_pagecontrol(Height=300,  Width=400)

        #      - - - - -
        LayTab1 = get_layout(layout_type='vstack', Left=0,  Height=20,  Top=0,  Width=20, 
                         TopMargin=6, RightMargin=6, BottomMargin=6, LeftMargin=6)
        LayTab1.add_widget( get_edit(widget_name='Get What', label_text='', initial_value='No Label') )

        LayTab1.add_widget( get_edit(widget_name='Get Stuff', 
                                 label_text='Enter Stuff', initial_value='Has Label') )
        Tab1 = get_tabsheet(layout=LayTab1, Caption='My 1st Tab')
        Page.add_tabsheet( Tab1 )
        #      - - - - -
        LayTab2 = get_layout(layout_type='vstack', Left=0,  Height=20,  Top=0,  Width=20, 
                         TopMargin=6, RightMargin=6, BottomMargin=6, LeftMargin=6)
        LayTab2.add_widget( get_edit(widget_name='Get What', label_text='', initial_value='No Label #2') )

        LayTab2.add_widget( get_edit(widget_name='Get Stuff #2', 
                                 label_text='Enter Stuff #2', initial_value='Has Label #2') )
        Tab2 = get_tabsheet(layout=LayTab2, Caption='My 2nd Tab')
        Page.add_tabsheet( Tab2 )
        #      - - - - -


        Lay.add_widget( Page )
        # ===================

        Lay.add_widget( get_edit(edit_type='other', widget_name='GetValue',  
                        initial_value='VLayout Wrapped', label_text='xxx') )
        Lay.add_widget( get_edit(widget_name='Get Other Stuff', 
                                 label_text='Enter Other Stuff', initial_value='LabeledEdit') )


        Lay.summ_print()
        print '='*55

        F = get_form( form_name='MyForm1', layout=Lay,
                  Left=800,  Height=240,  Top=10,  Width=320, 
                  Caption=None,  LCLVersion='1.6.0.4')

        C = get_gui(project_name='ProjWhat', form1_obj=F)
        
        #C.save_project_files( path_name=os.path.join(here,'chk_pg'), over_write_OK=True )
    
    def test_factory(self):
        Lay = get_layout(layout_type='vstack', Left=41,  Height=0,  Top=42,  Width=0, 
                         TopMargin=6, RightMargin=6, BottomMargin=6, LeftMargin=6)

        
        Lay.add_widget( get_radiogroup(Items=None, ItemIndex=1) )
        
        Lay.add_widget( get_label( widget_name='Get_Text', Caption='Label for Get_Text', BottomMargin=0) )
        Lay.add_widget( get_button(widget_name='Do Wide Things', Width=100, TopMargin=0) )

        Lay.add_widget( get_edit(widget_name='Get What', label_text='', initial_value='No Label') )

        Lay.add_widget( get_edit(widget_name='Get Stuff', 
                                 label_text='Enter Stuff', initial_value='Has Label') )
        
        # - - - -
        LayH = get_layout(layout_type='hstack', Left=41,  Height=0,  Top=42,  Width=0, 
                         TopMargin=6, RightMargin=6, BottomMargin=6, LeftMargin=6)
        LayH.add_widget( get_edit(widget_name='Get Other Stuff', 
                                 label_text='Enter Other Stuff', initial_value='LabeledEdit') )

        LayH.add_widget( get_edit(edit_type='other', widget_name='GetValue',  
                        initial_value='HLayout Wrapped', label_text='xxx') )
        Lay.add_widget( get_panel(layout=LayH) )
        
        # - - - -

        Page = get_pagecontrol(Height=300,  Width=400)

        #      - - - - -
        LayTab1 = get_layout(layout_type='vstack', Left=0,  Height=20,  Top=0,  Width=20, 
                         TopMargin=6, RightMargin=6, BottomMargin=6, LeftMargin=6)
        LayTab1.add_widget( get_edit(widget_name='Get What', label_text='', initial_value='No Label') )

        LayTab1.add_widget( get_edit(widget_name='Get Stuff', 
                                 label_text='Enter Stuff', initial_value='Has Label') )
        Tab1 = get_tabsheet(layout=LayTab1, Caption='My 1st Tab')
        Page.add_tabsheet( Tab1 )
        #      - - - - -
        LayTab2 = get_layout(layout_type='vstack', Left=0,  Height=20,  Top=0,  Width=20, 
                         TopMargin=6, RightMargin=6, BottomMargin=6, LeftMargin=6)
        LayTab2.add_widget( get_edit(widget_name='Get What', label_text='', initial_value='No Label #2') )

        LayTab2.add_widget( get_edit(widget_name='Get Stuff #2', 
                                 label_text='Enter Stuff #2', initial_value='Has Label #2') )
        Tab2 = get_tabsheet(layout=LayTab2, Caption='My 2nd Tab')
        Page.add_tabsheet( Tab2 )
        #      - - - - -


        Lay.add_widget( Page )        

        Lay.summ_print()
        print '='*55

        F = get_form( form_name='MyForm1', layout=Lay,
                  Left=611,  Height=240,  Top=162,  Width=320, 
                  Caption=None,  LCLVersion='1.6.0.4')

        C = get_gui(project_name='ProjWhat', form1_obj=F)

        C.save_project_files( path_name=os.path.join(here,'chk_factory'), over_write_OK=True )
        


if __name__ == '__main__':
    # Can test just this file from command prompt
    #  or it can be part of test discovery from nose, unittest, pytest, etc.
    unittest.main()

