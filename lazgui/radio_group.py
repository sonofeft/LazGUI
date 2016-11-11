

from widget import Widget

class RadioGroup( Widget ):

    def __init__(self, Items=None, ItemIndex=0,
                 widget_name='MyChoice', Left=0,  Height=100,  Top=0,  Width=200, 
                 TopMargin=10, RightMargin=10, BottomMargin=10, LeftMargin=10,
                 Caption='Pick One', has_OnClick=False, has_OnSelectionChanged=True,
                 AutoSize=True):
        
        super(RadioGroup, self).__init__(widget_type='RadioGroup', 
                                     widget_name=widget_name, Left=Left, Height=Height, 
                                     Top=Top, Width=Width, Caption=Caption, 
                                     has_OnClick=has_OnClick, has_OnChange=False,
                                     has_OnSelectionChanged=has_OnSelectionChanged,
                                     TopMargin=TopMargin, RightMargin=RightMargin, 
                                     BottomMargin=BottomMargin, LeftMargin=LeftMargin,
                                     AutoSize=AutoSize)
                                     
        if not type(Items)==list:
            self.Items = ['default option #1','default option #2','default option #3']
        else:
            self.Items = Items # should be a list of strings
        self.ItemIndex = ItemIndex
        self.AutoFill = True
        
        self.value_type = type( self.Items[0] )
        self.initial_value = self.Items[ItemIndex]
        
       
       
    def lfm_file_contents(self):
        """lfm files define form elements. Kind of a hierarchical config file."""

        pad = '  '*self.indent
        
        sL = [pad+'  object %s: T%s'%(self.full_widget_name, self.widget_type)  ]
        
        for s in ['Left','Height','Top','Width','AutoSize',
                  'OnClick','OnSelectionChanged','TabOrder','ItemIndex','AutoFill']:
            a = getattr(self, s, None)
            if not a is None:
                if s in ['Caption','Text']:
                    sL.append( "    %s = '%s'"%(s,a) )
                else:
                    sL.append( '    %s = %s'%(s,a) )
        
        sL.append(pad+"    ChildSizing.LeftRightSpacing = 6")
        sL.append(pad+"    ChildSizing.EnlargeHorizontal = crsHomogenousChildResize")
        sL.append(pad+"    ChildSizing.EnlargeVertical = crsHomogenousChildResize")
        sL.append(pad+"    ChildSizing.ShrinkHorizontal = crsScaleChilds")
        sL.append(pad+"    ChildSizing.ShrinkVertical = crsScaleChilds")
        sL.append(pad+"    ChildSizing.Layout = cclLeftToRightThenTopToBottom")
        sL.append(pad+"    ChildSizing.ControlsPerLine = 1")
        
        sL.append(pad+"    Items.Strings = (")
        for item in self.Items:
            sL.append(pad+"      '%s'"%str(item))
        sL.append(pad+"    )")
        
                    
        sL.append('  end')
        return '\n'.join(sL) + '\n'
                 
 

if __name__ == '__main__':
    
    ItemL = None#['First Choice','Second Pick','Third One','Last One']
    F = RadioGroup(  Items=ItemL, ItemIndex=2,
                 widget_name='MyChoice', Left=0,  Height=100,  Top=0,  Width=200, 
                 TopMargin=10, RightMargin=10, BottomMargin=10, LeftMargin=10,
                 Caption='Pick One', has_OnClick=False, has_OnSelectionChanged=True,
                 AutoSize=True)
                 
    print F.pas_file_implement()
    print '='*55
    print F.lfm_file_contents()