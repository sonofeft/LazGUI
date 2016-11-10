"""
Layout can be a Canvas, Dock, Grid, HStackPanel, VStackPanel or WrapPanel

see: https://msdn.microsoft.com/en-us/library/ms745058(v=vs.110).aspx
"""

class Layout( object ):
    
    def __init__(self, Left=0,  Height=20,  Top=0,  Width=20, 
                 TopMargin=6, RightMargin=6, BottomMargin=6, LeftMargin=6):
                 
        self.Left = Left
        self.Height = Height # usually starts at zero until Widget objects are added
        self.Top = Top
        self.Width = Width # usually starts at zero until Widget objects are added
        
        self.TopMargin = TopMargin
        self.RightMargin = RightMargin
        self.BottomMargin = BottomMargin
        self.LeftMargin = LeftMargin        
        
        self.ActualHeight = Height + TopMargin + BottomMargin
        self.ActualWidth =  Width  + LeftMargin + RightMargin
        self.set_bbox()
        
        self.widgetL = [] # Usually order is important
        
        self.full_widget_name = 'Layout'
        self.indent = 0
        
    def set_indent(self, indent):
        self.indent = indent
        for widget in self.widgetL:
            widget.set_indent( self.indent )
        
    def get_full_widgetL(self):
        widgetL = []
        for W in self.widgetL:
            #try:
            widgetL.extend( W.get_full_widgetL() )
            #except:
            #    print 'ERROR with W.get_full_widgetL() for W =',W
        return widgetL

        
    def get_top_level_widgetL(self):
        return self.widgetL[:]

    def append_widget_or_layout(self, widget):
        """Some Widget objects require additional "helper" Widgets in another Layout 
           (No longer intercepting widget definitions)
        """
        
        self.widgetL.append( widget )
        return widget
        
    
    def add_widget(self, widget):
        """Acts like a Canvas, leaving Widgets in original orientation."""
        
        widget.set_top_left(Top=self.Top+widget.Top,  Left=self.Left+widget.Left)
        self.adjust_bbox_for_widget( widget )
        #self.widgetL.append( widget )
        widget.set_indent( self.indent )
        
        return self.append_widget_or_layout( widget ) # for calls like: B = Lay.add_widget( Button() ) 
        
    def recalc(self):
        """Any changes to location of layout requires a recalc"""
        self.set_bbox() # uses current self.Top and self.Left
        for widget in self.widgetL:
            widget.set_top_left(Top=self.Top+widget.Top,  Left=self.Left+widget.Left)
            self.adjust_bbox_for_widget( widget )
            
            widget.set_indent( self.indent + 1 )

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
                     
    def set_bbox_upper_left(self, BBTop=10, BBLeft=10):
        self.Top = BBTop + self.TopMargin
        self.Left = BBLeft + self.LeftMargin
        self.set_bbox()
        self.recalc()
        
    def summ_print(self):
        print '='*55
        print self.full_widget_name,' BBox=',self.BBox
        outL = []
        for widget in self.widgetL:
            outL.append( ['Left=%3i'%widget.Left, 'Top=%3i'%widget.Top, 
                          widget.full_widget_name, 'BBox=%s'%widget.BBox, 
                          'AW=%s'%widget.ActualWidth, 'AH=%s'%widget.ActualHeight] )
        for L in sorted(outL):
            print '   '.join( ['%s'%s for s in L] )

    def lfm_file_contents(self):
        sL = []
            
        itab = 0
        for w in self.widgetL:
            if hasattr(w, 'TabOrder'):
                w.TabOrder = itab
                itab += 1
            if hasattr(w, 'TabOrder') or hasattr(w, 'Caption'):
                sL.append( w.lfm_file_contents() )
            
        sOut = '\n'.join(sL) + '\n'
        sOut = sOut.replace('\n\n','\n')
        return sOut
        

class GridPanel( Layout ):
    
    def __init__(self, Left=0,  Height=0,  Top=10,  Width=0, 
                 TopMargin=6, RightMargin=6, BottomMargin=6, LeftMargin=6):

        super(GridPanel, self).__init__( Left=Left, Height=Height, Top=Top, 
                                           Width=Width, TopMargin=TopMargin, 
                                           RightMargin=RightMargin, BottomMargin=BottomMargin, 
                                           LeftMargin=LeftMargin)
                                           
        self.grid_rowcolD = {} # index=widget object, value=(row,col)
        self.grid_widgetD = {} # index=(row,col), value=widget object
        self.full_widget_name = 'Grid Layout'
    
        
    def add_widget(self, widget, row=0, col=0):
        """Arrange widgets in grid.
           If more than one widget is in a cell, arrange them as VStackPanel members.
        """
        row_col = (row,col)
        self.grid_rowcolD[widget] = row_col
        #self.widgetL.append( widget )
        widget = self.append_widget_or_layout( widget )
        
        # get list of widgets from (row,col) tuple
        if row_col in self.grid_widgetD:
            self.grid_widgetD[row_col].append( widget )
        else:
            self.grid_widgetD[row_col] = [ widget ]
        
        self.recalc()
        return widget # for calls like: B = Lay.add_widget( Button() ) 
        
    def recalc(self):
        """Any changes to location of layout requires a recalc"""
        self.set_bbox() # uses current self.Top and self.Left
        
        rowHtD = {} # index=row, value=max ActualHeight in row
        colWdD = {} # index=col, value=max ActualWidth in col
        #print 'self.grid_widgetD =',self.grid_widgetD
        #print 'self.grid_rowcolD =',self.grid_rowcolD
        
        # initialize row column H W values
        for row_col in self.grid_widgetD.keys():
            row,col = row_col
            rowHtD[row] = 0
            colWdD[col] = 0

        # Figure out Width and Height of each specified row and col
        for row_col, wL in self.grid_widgetD.items():
            row,col = row_col
            w,h = 0,0
            for widget in wL:
                w = max(w, widget.ActualWidth)
                h += widget.ActualHeight
            rowHtD[row] = max(rowHtD[row], h)
            colWdD[col] = max(colWdD[col], w)
            #if len(wL)>1:
            #    print ' ==> Multiple Widgets in Row/Col =',row_col,'w=%i, h=%i'%(w,h)
        #print 'rowHtD =',rowHtD
        #print 'colWdD =',colWdD
        
        # create dict object for each row and col reference
        #   to get Top/Left position for each (row,col)
        def make_posL( rcL, rcD ):
            outL = [0]
            for p in rcL[:-1]:
                outL.append( outL[-1] + rcD[p] )
            return outL
        
        rowL = sorted( rowHtD.keys() )
        row_posL = make_posL( rowL, rowHtD )
        row_posD = {}
        for row, pos in zip(rowL, row_posL):
            row_posD[row] = pos
        
        colL = sorted( colWdD.keys() )
        col_posL = make_posL( colL, colWdD )
        col_posD = {}
        for col, pos in zip(colL, col_posL):
            col_posD[col] = pos
        
        #print 'row_posL, D =',row_posL, row_posD
        #print 'col_posL, D =',col_posL, col_posD
        
        # Calc positions for each widget.
        for row_col, wL in self.grid_widgetD.items():
            row,col = row_col
            dy = 0
            for widget in wL:
                x0 = self.Left + col_posD[col]
                y0 = self.Top + row_posD[row] + dy
                dy += widget.ActualHeight
                widget.set_bbox_upper_left(BBTop=y0,  BBLeft=x0)
                
                self.adjust_bbox_for_widget( widget )



class VStackPanel( Layout ):
    
    def __init__(self, Left=0,  Height=0,  Top=10,  Width=0, 
                 TopMargin=6, RightMargin=6, BottomMargin=6, LeftMargin=6):

        super(VStackPanel, self).__init__( Left=Left, Height=Height, Top=Top, 
                                           Width=Width, TopMargin=TopMargin, 
                                           RightMargin=RightMargin, BottomMargin=BottomMargin, 
                                           LeftMargin=LeftMargin)
        self.full_widget_name = 'VStackPanel Layout'

        
    def add_widget(self, widget):
        """Arrange widgets in Vertical Stack."""
        
        if len(self.widgetL)==0:
            x0 = self.Left
            y1 = self.Top
        else:
            x0,y0,x1,y1 = self.widgetL[-1].BBox
            #x0 = x0 - self.Left
            #y1 = y1 - self.Top
        widget = self.append_widget_or_layout( widget ) #self.widgetL.append( widget )
        
        #if isinstance(widget,VStackPanel):
        #    print 'VStackPanel setting BBox upper left to BBTop=%i,  BBLeft=%i'%(y1,  x0)
        #    print '  widget Height=%i,  ActualHeight=%i'%(widget.Height, widget.ActualHeight)
        widget.set_bbox_upper_left(BBTop=y1,  BBLeft=x0)
        #if isinstance(widget,VStackPanel):
        #    print '  widget=',widget,'BBox=',widget.BBox
        #    print '                   self BBox=',self.BBox
        self.adjust_bbox_for_widget( widget )
        #if isinstance(widget,VStackPanel):
        #    print '          adjusted self BBox=',self.BBox
        
        return widget # for calls like: B = Lay.add_widget( Button() ) 
        
    def recalc(self):
        """Any changes to location of layout requires a recalc"""
        self.set_bbox() # uses current self.Top and self.Left
        for i,widget in enumerate(self.widgetL):        
            if i==0:
                x0 = self.Left
                y1 = self.Top
            else:
                x0,y0,x1,y1 = self.widgetL[i-1].BBox
            
            widget.set_bbox_upper_left(BBTop=y1,  BBLeft=x0)
            self.adjust_bbox_for_widget( widget )


class HStackPanel( Layout ):
    
    def __init__(self, Left=0,  Height=0,  Top=10,  Width=0, 
                 TopMargin=6, RightMargin=6, BottomMargin=6, LeftMargin=6):

        super(HStackPanel, self).__init__( Left=Left, Height=Height, Top=Top, 
                                           Width=Width, TopMargin=TopMargin, 
                                           RightMargin=RightMargin, BottomMargin=BottomMargin, 
                                           LeftMargin=LeftMargin)
        self.full_widget_name = 'HStackPanel Layout'
        
    def add_widget(self, widget):
        """Arrange widgets in Horizontal Stack."""
        
        if len(self.widgetL)==0:
            x1 = self.Left
            y0 = self.Top
        else:
            x0,y0,x1,y1 = self.widgetL[-1].BBox
            #x1 = x1 - self.Left
            #y0 = y0 - self.Top
        widget = self.append_widget_or_layout( widget ) #self.widgetL.append( widget )

        #print 'HStack setting BBox upper left to BBTop=%i,  BBLeft=%i'%(y0,  x1)
        widget.set_bbox_upper_left(BBTop=y0,  BBLeft=x1)
        #print '  widget=',widget,'BBox=',widget.BBox
        #print '                   self BBox=',self.BBox
        self.adjust_bbox_for_widget( widget )
        #print '          adjusted self BBox=',self.BBox
        
        return widget # for calls like: B = Lay.add_widget( Button() ) 
        
    def recalc(self):
        """Any changes to location of layout requires a recalc"""
        self.set_bbox() # uses current self.Top and self.Left
        for i,widget in enumerate(self.widgetL):        
            if i==0:
                x1 = self.Left
                y0 = self.Top
            else:
                x0,y0,x1,y1 = self.widgetL[i-1].BBox
            
            widget.set_bbox_upper_left(BBTop=y0,  BBLeft=x1)
            self.adjust_bbox_for_widget( widget )
            
            #print "Adjusted HStackPanel's",widget.full_widget_name,'y0=%i'%y0,'x1=%i'%x1


if __name__ == '__main__':
    from widget import Widget
    
    GP = GridPanel( )
    for i in [3,5,9]:
        for j in [2,6,8]:
            GP.add_widget( Widget( widget_type='Button'), row=i, col=j )
    
    GP.add_widget( Widget( widget_type='Button',  Width=100), row=5, col=6 )        
