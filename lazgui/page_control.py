

from widget import Widget
from panel import Panel

class PageControl( Widget ):

    def __init__(self, 
                 widget_name='MyPageControl', Left=0,  Height=100,  Top=0,  Width=200, 
                 TopMargin=10, RightMargin=10, BottomMargin=10, LeftMargin=10,
                 Caption=None, 
                 AutoSize=False):
        
        super(PageControl, self).__init__(widget_type='PageControl', 
                                     widget_name=widget_name, Left=Left, Height=Height, 
                                     Top=Top, Width=Width, Caption=Caption, 
                                     has_OnClick=False, has_OnChange=False,
                                     TopMargin=TopMargin, RightMargin=RightMargin, 
                                     BottomMargin=BottomMargin, LeftMargin=LeftMargin,
                                     AutoSize=AutoSize)
                                     
        del self.Caption # don't want a caption
        del self.TabOrder
        del self.AutoSize
        self.ActivePage = ''
        self.TabIndex = 0
        self.TabOrder = 0
        
    def add_tabsheet(self, tab_sheet):
        
        self.child_widgetL.append( tab_sheet )
        tab_sheet.set_indent( self.indent + 1 )
        self.ActivePage = self.child_widgetL[0].full_widget_name # set 1st tab as active page
        
        tab_sheet.ClientHeight = self.Height - 28
        tab_sheet.ClientWidth =  self.Width - 8
                     
class TabSheet( Panel ):
    """A PageControl object with TabSheet objects attached"""
    
    def __init__(self, layout=None, Caption='TabSheet1',
                 widget_name='MyTabSheet', Left=0,  Height=25,  Top=0,  Width=75, 
                 TopMargin=10, RightMargin=10, BottomMargin=10, LeftMargin=10,
                 has_OnClick=False, has_OnChange=False,
                 AutoSize=False):
        
        super(TabSheet, self).__init__(layout=layout,
                                     widget_name=widget_name, Left=Left, Height=Height, 
                                     Top=Top, Width=Width, 
                                     has_OnClick=has_OnClick, has_OnChange=has_OnChange,
                                     TopMargin=TopMargin, RightMargin=RightMargin, 
                                     BottomMargin=BottomMargin, LeftMargin=LeftMargin,
                                     AutoSize=AutoSize)
        self.widget_type = 'TabSheet'
        self.Caption = Caption
        del self.AutoSize
        del self.Left 
        del self.Top 
        del self.Width
        del self.Height
        

if __name__ == '__main__':
    from button import Button
    from edit import Edit
    from layout import VStackPanel, HStackPanel
    
    
    Lay = VStackPanel(Left=10,  Height=0,  Top=10,  Width=0, 
                          TopMargin=10, RightMargin=10, BottomMargin=10, LeftMargin=10)
                 
    Lay.add_widget( Edit( widget_name='Get_Text', initial_value='Hi') )
    Lay.add_widget( Edit( widget_name='Get_Int', initial_value=3) )
    Lay.add_widget( Edit( widget_name='Get_Float', initial_value=5.55) )
    Lay.add_widget( Edit( widget_name='Get_Bool', initial_value=True) )
    
    P = PageControl(widget_name='MyPageControl', Left=0,  Height=100,  Top=0,  Width=200)
    P.add_tabsheet( TabSheet(  layout=Lay,
                widget_name='MyTab1', Left=41,  Height=25,  Top=42,  Width=75) )
    #print 'child_widgetL =',P.child_widgetL
    Lay = HStackPanel(Left=10,  Height=0,  Top=10,  Width=0, 
                          TopMargin=10, RightMargin=10, BottomMargin=10, LeftMargin=10)
                 
    Lay.add_widget( Edit( widget_name='Get_Text', initial_value='Hi') )
    Lay.add_widget( Edit( widget_name='Get_Int', initial_value=3) )
    P.add_tabsheet( TabSheet(  layout=Lay,
                widget_name='MyTab2', Left=41,  Height=25,  Top=42,  Width=75) )
                 
    print P.pas_file_implement()
    print '='*55
    print P.lfm_file_contents()