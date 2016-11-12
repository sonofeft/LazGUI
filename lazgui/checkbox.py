"""Represents an object on a Form (eg. Button, Label, etc.)"""

from widget import Widget

class CheckBox( Widget ):
    
    def __init__(self, Checked=False,
                 widget_name='Generic', Left=0,  Height=25,  Top=0,  Width=75, 
                 TopMargin=10, RightMargin=10, BottomMargin=10, LeftMargin=10,
                 Caption=None, has_OnClick=True, has_OnChange=False,
                 AutoSize=True):
        
        super(CheckBox, self).__init__(widget_type='CheckBox', 
                                     widget_name=widget_name, Left=Left, Height=Height, 
                                     Top=Top, Width=Width, Caption=Caption, 
                                     has_OnClick=has_OnClick, has_OnChange=has_OnChange,
                                     TopMargin=TopMargin, RightMargin=RightMargin, 
                                     BottomMargin=BottomMargin, LeftMargin=LeftMargin,
                                     AutoSize=AutoSize)
        self.Checked = Checked

if __name__ == '__main__':
    
    F = CheckBox( widget_name='DoSompin', Left=41,  Height=25,  Top=42,  Width=75, 
                 Caption=None, has_OnClick=True)
                 
    print F.pas_file_implement()
    print '='*55
    print F.lfm_file_contents()