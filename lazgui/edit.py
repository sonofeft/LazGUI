"""Represents an object on a Form (eg. Button, Label, etc.)"""

from widget import Widget

class Edit( Widget ):
    
    def __init__(self, 
                 widget_name='GetValue',  initial_value='aBc', label_text='',
                 Left=0,  Height=23,  Top=0,  Width=80, 
                 TopMargin=10, RightMargin=10, BottomMargin=10, LeftMargin=10,
                 has_OnClick=False, has_OnChange=True,
                 AutoSize=False):
        
        super(Edit, self).__init__(widget_type='Edit', 
                                     widget_name=widget_name, Left=Left, Height=Height, 
                                     Top=Top, Width=Width, 
                                     has_OnClick=has_OnClick, has_OnChange=has_OnChange,
                                     TopMargin=TopMargin, RightMargin=RightMargin, 
                                     BottomMargin=BottomMargin, LeftMargin=LeftMargin,
                                     AutoSize=AutoSize, label_text=label_text)
                                     
        self.initial_value = initial_value
        self.Text = str( self.initial_value )
        self.value_type = type( initial_value )
        self.Caption = None # label_text will result in a Label object being added
                 

if __name__ == '__main__':
    
    F = Edit( widget_name='Get_Text', initial_value=5.5,
                 Left=41,  Height=25,  Top=42,  Width=75, 
                 has_OnClick=True)
                 
    print F.pas_file_implement()
    print '='*55
    print F.lfm_file_contents()