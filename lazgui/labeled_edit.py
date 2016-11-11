"""Represents an object on a Form (eg. Button, Label, etc.)"""

from widget import Widget

class LabeledEdit( Widget ):
    
    def __init__(self, label_text='Enter Value', initial_value=123,
                 widget_name='GetDiam', Left=0,  Height=23,  Top=0,  Width=80, 
                 TopMargin=24, RightMargin=10, BottomMargin=10, LeftMargin=10,
                 Caption=None, has_OnClick=False, has_OnChange=True,
                 AutoSize=False, grow_for_long_text=True):
        
        super(LabeledEdit, self).__init__(widget_type='LabeledEdit', 
                                     widget_name=widget_name, Left=Left, Height=Height, 
                                     Top=Top, Width=Width, Caption=Caption, 
                                     has_OnClick=has_OnClick, has_OnChange=has_OnChange,
                                     TopMargin=TopMargin, RightMargin=RightMargin, 
                                     BottomMargin=BottomMargin, LeftMargin=LeftMargin,
                                     AutoSize=AutoSize, grow_for_long_text=grow_for_long_text)
                                     
        self.initial_value = initial_value
        self.Text = str( self.initial_value )
        self.value_type = type( initial_value )
        
        self.grow_for_long_text = grow_for_long_text
        self.label_text = label_text

        self.Width = Width
        if self.grow_for_long_text:
            for s in [label_text, self.Text]:
                sugg_len = 10.0 + len(s) * 75.0 / 11.0
                
                if sugg_len > self.Width:
                    self.Width = int(sugg_len) + 1
                    #print 'Suggested length for LabeledEdit is',self.Width

    def lfm_file_contents(self):
        """lfm files define form elements. Kind of a hierarchical config file."""
        
        pad = '  '*self.indent
        
        sL = [pad+'  object %s: T%s'%(self.full_widget_name, self.widget_type)  ]
        
        for s in ['Left','Height','Top','Width','AutoSize',
                  'OnClick','OnChange','TabOrder','Text']:
            a = getattr(self, s, None)
            if not a is None:
                if s in ['Caption','Text']:
                    sL.append( pad+"    %s = '%s'"%(s,a) )
                else:
                    sL.append( pad+'    %s = %s'%(s,a) )
        
        
        sL.append(pad+"    EditLabel.AnchorSideLeft.Control = %s"%self.full_widget_name )
        sL.append(pad+"    EditLabel.AnchorSideRight.Control = %s"%self.full_widget_name )
        sL.append(pad+"    EditLabel.AnchorSideRight.Side = asrBottom" )
        sL.append(pad+"    EditLabel.AnchorSideBottom.Control = %s"%self.full_widget_name )
        sL.append(pad+"    EditLabel.Left = %s"%self.Left )
        sL.append(pad+"    EditLabel.Height = %s"%(self.Height - 8,) )
        sL.append(pad+"    EditLabel.Top = %s"%(self.Top - 22,) )
        sL.append(pad+"    EditLabel.Width = %s"%self.Width )
        sL.append(pad+"    EditLabel.Caption = '%s'"%self.label_text )
        sL.append(pad+"    EditLabel.ParentColor = False" )
        sL.append(pad+"    TabOrder = %s"%self.TabOrder )
        #sL.append(pad+"    Text = '%s'"%self.initial_value )
                    
        sL.append(pad+'  end')
        return '\n'.join(sL) + '\n'
                 



if __name__ == '__main__':
    
    F = LabeledEdit( label_text='Enter Diameter', widget_name='GetDiam', 
                     initial_value=4.567,   
                     Left=41,  Height=23,  Top=84,  Width=80, 
                     Caption=None, has_OnClick=True)
                 
    print F.pas_file_implement()
    print '='*55
    print F.lfm_file_contents()