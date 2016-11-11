"""This is the factory function for all GUI elements"""
import inspect

from laz_gui import LazarusGUI
from form import Form
from button import Button
from edit import Edit
from label import Label
from labeled_edit import LabeledEdit
from layout import Layout, VStackPanel, HStackPanel, GridPanel
from panel import Panel
from page_control import PageControl, TabSheet
from radio_group import RadioGroup

def key_word_args(paramL, local_dict):
    """Make a dict of key word arguements with their call values"""
    kwargs = {}
    for param in paramL:
        kwargs[param] = local_dict[param]
    return kwargs
    

# ============================== RadioGroup ======================================
def get_radiogroup(Items=None, ItemIndex=0,
                 widget_name='MyChoice', Left=0,  Height=100,  Top=0,  Width=200, 
                 TopMargin=10, RightMargin=10, BottomMargin=10, LeftMargin=10,
                 Caption='Pick One', has_OnClick=False, has_OnSelectionChanged=True,
                 AutoSize=True):
        
    return RadioGroup( **key_word_args(RADIOGROUP_PARAML, locals()) )
                   
RADIOGROUP_PARAML = inspect.getargspec( get_radiogroup )[0]

    
# ============================== PageControl ======================================
def get_pagecontrol(widget_name='MyPageControl', Left=0,  Height=100,  Top=0,  Width=200, 
                 TopMargin=10, RightMargin=10, BottomMargin=10, LeftMargin=10,
                 Caption=None, 
                 AutoSize=False):
        
    return PageControl( **key_word_args(PAGECONTROL_PARAML, locals()) )
                   
PAGECONTROL_PARAML = inspect.getargspec( get_pagecontrol )[0]

# ============================== TabSheet ======================================
def get_tabsheet(layout=None, Caption='TabSheet1',
                 widget_name='MyTabSheet', Left=0,  Height=25,  Top=0,  Width=75, 
                 TopMargin=10, RightMargin=10, BottomMargin=10, LeftMargin=10,
                 has_OnClick=False, has_OnChange=False,
                 AutoSize=False):
        
    return TabSheet( **key_word_args(TABSHEET_PARAML, locals()) )
                   
TABSHEET_PARAML = inspect.getargspec( get_tabsheet )[0]

# ============================== Panel ======================================
def get_panel(layout=None,
              widget_name='MyPanel', Left=0,  Height=25,  Top=0,  Width=75, 
              TopMargin=10, RightMargin=10, BottomMargin=10, LeftMargin=10,
              has_OnClick=False, has_OnChange=False,
              AutoSize=False):
        
    return Panel( **key_word_args(PANEL_PARAML, locals()) )
                   
PANEL_PARAML = inspect.getargspec( get_panel )[0]

# ============================== Edit Box ======================================
def get_edit(edit_type='default', 
             widget_name='GetValue',  initial_value='aBc', label_text='',
             Left=0,  Height=23,  Top=0,  Width=80, 
             TopMargin=10, RightMargin=10, BottomMargin=10, LeftMargin=10,
             has_OnClick=False, has_OnChange=True,
             AutoSize=False):
    
    if label_text:
        if edit_type == 'default':
            return LabeledEdit( **key_word_args(EDIT_PARAML, locals()) )
        else:
            VLay = VStackPanel( )
            VLay.add_widget( Label( widget_name=widget_name+'Label', Caption=label_text, BottomMargin=0) )
            widget = Edit( **key_word_args(EDIT_PARAML, locals()) )
            widget.TopMargin = 0
            widget.label_text = ''
            VLay.add_widget( widget )
            return VLay
            
    else:
        return Edit( **key_word_args(EDIT_PARAML, locals()) )
                   
EDIT_PARAML = inspect.getargspec( get_edit )[0]
EDIT_PARAML.remove( 'edit_type' )
# ============================== Button ======================================
def get_button(widget_name='Generic', Left=0,  Height=25,  Top=0,  Width=75, 
               TopMargin=10, RightMargin=10, BottomMargin=10, LeftMargin=10,
               Caption=None, has_OnClick=True, has_OnChange=False,
               AutoSize=False):
        
    return Button( **key_word_args(BUTTON_PARAML, locals()) )
                   
BUTTON_PARAML = inspect.getargspec( get_button )[0]
# ============================== Label ======================================
def get_label(widget_name='MyLabel', Left=0,  Height=25,  Top=0,  Width=75, 
              TopMargin=10, RightMargin=10, BottomMargin=10, LeftMargin=10,
              Caption='My Caption', has_OnClick=False, has_OnChange=False,
              AutoSize=True):
        
    return Label( **key_word_args(LABEL_PARAML, locals()) )
                   
LABEL_PARAML = inspect.getargspec( get_label )[0]

# ============================== Layout ======================================
def get_layout(layout_type='vstack', Left=0,  Height=20,  Top=0,  Width=20, 
               TopMargin=6, RightMargin=6, BottomMargin=6, LeftMargin=6):
    
    lc_type = layout_type.lower()
    if lc_type == 'vstack':
        return VStackPanel( **key_word_args(LAYOUT_PARAML, locals()) )
    elif lc_type == 'hstack':
        return HStackPanel( **key_word_args(LAYOUT_PARAML, locals()) )
    elif lc_type == 'grid':
        return GridPanel( **key_word_args(LAYOUT_PARAML, locals()) )
    elif lc_type == 'canvas':
        return Layout( **key_word_args(LAYOUT_PARAML, locals()) )
    else:
        print '='*30,'WARNING','='*30
        print '  bad layout_type in call to get_layout, Illegal layout_type = "%s"'%layout_type
        print '  Using Vertical Stack layout by default = "vstack"'
        print '='*30,'WARNING','='*30
        return VStackPanel( **key_word_args(LAYOUT_PARAML, locals()) )
        
LAYOUT_PARAML = inspect.getargspec( get_layout )[0]
LAYOUT_PARAML.remove( 'layout_type' )


# ============================== Form ======================================
def get_form(form_name='Form1', layout=None, has_file_menu=True,
             Left=611,  Height=240,  Top=162,  Width=320, 
             Caption=None,  LCLVersion='1.6.0.4'):
                 
    return Form( **key_word_args(FORM_PARAML, locals()) )
    
FORM_PARAML = inspect.getargspec( get_form )[0]

# ============================== LazarusGUI ======================================
def get_gui(project_name='project1', form1_obj=None, data_file_ext='proj_dat'):
                 
    return LazarusGUI( **key_word_args(GUI_PARAML, locals()) )
    
GUI_PARAML = inspect.getargspec( get_gui )[0]


if __name__ == "__main__":
    
    obj = get_edit(edit_type='default', widget_name='GetValue',  initial_value='aBc', label_text='')
    print obj
    obj = get_edit(edit_type='default', widget_name='GetValue',  initial_value='aBc', label_text='xxx')
    print obj
    obj = get_edit(edit_type='other', widget_name='GetValue',  initial_value='aBc', label_text='xxx')
    print obj
    
    print '-'*55
    
    obj = get_button()
    print obj
    
    obj = get_layout(layout_type='hstack',Left=123,  Height=123,  Top=123,  Width=123, 
                     TopMargin=123, RightMargin=123, BottomMargin=123, LeftMargin=123)
    print obj
    obj = get_layout(layout_type='xxx',Left=123,  Height=123,  Top=123,  Width=123, 
                     TopMargin=123, RightMargin=123, BottomMargin=123, LeftMargin=123)
    