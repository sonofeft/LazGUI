"""Represents an object on a Form (eg. Button, Label, etc.)"""

from widget import Widget

class Panel( Widget ):
    
    def __init__(self, layout=None,
                 widget_name='MyPanel', Left=0,  Height=25,  Top=0,  Width=75, 
                 TopMargin=10, RightMargin=10, BottomMargin=10, LeftMargin=10,
                 has_OnClick=False, has_OnChange=False,
                 AutoSize=False):
        
        super(Panel, self).__init__(widget_type='Panel', 
                                     widget_name=widget_name, Left=Left, Height=Height, 
                                     Top=Top, Width=Width, 
                                     has_OnClick=has_OnClick, has_OnChange=has_OnChange,
                                     TopMargin=TopMargin, RightMargin=RightMargin, 
                                     BottomMargin=BottomMargin, LeftMargin=LeftMargin,
                                     AutoSize=AutoSize)
        self.widget_type = 'Panel'
                
        del self.Caption # don't want a caption in the middle of the Panel
        del self.TabOrder

        self.layout = layout
        if not layout is None:
            self.child_widgetL.append( layout )
            layout.set_indent( self.indent + 1 )
        #    
        #    for w in layout.get_full_widgetL():
        #        self.adjust_bbox_for_widget( w )
        
        
            # if layout is bigger than form, increase size of form
            H = layout.ActualHeight + layout.Top + layout.BottomMargin
            if self.Height < H:
                print 'Increasing Height from',self.Height,'to',H
                self.Height = H
                
            W = layout.ActualWidth + layout.Left + layout.RightMargin
            if self.Width < W:
                print 'Increasing Width from',self.Width,'to',W
                self.Width = W
            self.ClientHeight = self.Height
            self.ClientWidth = self.Width
        

        
    def recalc(self):
        """Any changes to location of layout requires a recalc"""
        self.set_bbox() # uses current self.Top and self.Left
        for widget in self.widgetL:
            widget.set_top_left(Top=self.Top+widget.Top,  Left=self.Left+widget.Left)
            self.adjust_bbox_for_widget( widget )

    def adjust_bbox_for_widget(self, widget):
        #print 'in adjust_bbox_for_widget:',widget, widget.BBox
        self.BBox[0] = min(self.BBox[0], widget.BBox[0])
        self.BBox[1] = min(self.BBox[1], widget.BBox[1])
        self.BBox[2] = max(self.BBox[2], widget.BBox[2])
        self.BBox[3] = max(self.BBox[3], widget.BBox[3])

        self.ActualHeight = self.BBox[3] - self.BBox[1]
        self.ActualWidth =  self.BBox[2] - self.BBox[0]

        self.Height = self.ActualHeight - self.TopMargin - self.BottomMargin
        self.Width = self.ActualWidth - self.LeftMargin - self.RightMargin
        # self.recalc() <=== endless loop

    
    def set_bbox(self):
        self.BBox = [self.Left-self.LeftMargin, 
                     self.Top-self.TopMargin, 
                     self.Left+self.Width+self.RightMargin, 
                     self.Top+self.Height+self.BottomMargin]
                     
        x0,y0,x1,y1 = self.BBox
        self.ActualHeight = y1 - y0
        self.ActualWidth =  x1 - x0
                     
    def set_top_left(self, Top=10, Left=10):
        self.Top = Top 
        self.Left = Left 
        self.set_bbox()
        self.recalc()
        
# ==============================================================


if __name__ == '__main__':
    from button import Button
    from edit import Edit
    from layout import VStackPanel
    
    Lay = VStackPanel(Left=10,  Height=0,  Top=10,  Width=0, 
                          TopMargin=10, RightMargin=10, BottomMargin=10, LeftMargin=10)
                 
    Lay.add_widget( Edit( widget_name='Get_Text', initial_value='Hi') )
    Lay.add_widget( Edit( widget_name='Get_Int', initial_value=3) )
    Lay.add_widget( Edit( widget_name='Get_Float', initial_value=5.55) )
    Lay.add_widget( Edit( widget_name='Get_Bool', initial_value=True) )
    
    F = Panel(  layout=Lay,
                widget_name='MyPanel', Left=41,  Height=25,  Top=42,  Width=75, 
                has_OnClick=True)
                 
    print F.pas_file_implement()
    print '='*55
    print F.lfm_file_contents()