

from widget import Widget

class ComboBox( Widget ):

    def __init__(self, Items=None, ItemIndex=0, ItemHeight=15,
                 widget_name='MyComboChoice', Left=0,  Height=100,  Top=0,  Width=200, 
                 TopMargin=10, RightMargin=10, BottomMargin=10, LeftMargin=10,
                 has_OnClick=False, has_OnSelect=True):
        
        super(ComboBox, self).__init__(widget_type='ComboBox', 
                                     widget_name=widget_name, Left=Left, Height=Height, 
                                     Top=Top, Width=Width, 
                                     has_OnClick=has_OnClick, has_OnChange=False,
                                     has_OnSelect=has_OnSelect,
                                     TopMargin=TopMargin, RightMargin=RightMargin, 
                                     BottomMargin=BottomMargin, LeftMargin=LeftMargin)
                                     
        if not type(Items)==list:
            self.Items = ['default option #1','default option #2','default option #3']
        else:
            self.Items = Items # should be a list of strings
        self.ItemIndex = ItemIndex
        self.AutoFill = True
        self.ItemHeight = ItemHeight
        
        self.value_type = type( self.Items[0] )
        self.initial_value = self.Items[ItemIndex]
        
       
       
    def lfm_file_contents(self):
        """lfm files define form elements. Kind of a hierarchical config file."""

        pad = '  '*self.indent
        
        sL = [pad+'  object %s: T%s'%(self.full_widget_name, self.widget_type)  ]
        
        for s in ['Left','Height','Top','Width', 'OnClick','OnSelect']:
            a = getattr(self, s, None)
            if not a is None:
                sL.append( '    %s = %s'%(s,a) )
                
        sL.append(pad+"    Items.Strings = (")
        for item in self.Items:
            sL.append(pad+"      '%s'"%str(item))
        sL.append(pad+"    )")

        # These need to come after Item.Strings
        for s in ['ItemHeight','TabOrder','ItemIndex']:
            a = getattr(self, s, None)
            if not a is None:
                sL.append( '    %s = %s'%(s,a) )

                    
        sL.append('  end')
        return '\n'.join(sL) + '\n'
                 
 

if __name__ == '__main__':
    
    ItemL = None#['First Choice','Second Pick','Third One','Last One']
    F = ComboBox(  Items=ItemL, ItemIndex=2,
                 widget_name='MyChoice', Left=0,  Height=100,  Top=0,  Width=200, 
                 TopMargin=10, RightMargin=10, BottomMargin=10, LeftMargin=10,
                 has_OnClick=False, has_OnSelect=True)
                 
    print F.pas_file_implement()
    print '='*55
    print F.lfm_file_contents()