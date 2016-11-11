"""Represents an object on a Form (eg. Button, Label, etc.)"""

def make_legal_name( name ):
    name = name.replace(' ','_')
    for c in '`~!@#$%^&*()_-=+?><,./|\\':
        name = name.replace(c,'_')
    return name


class Widget( object ):
    
    def change_full_name(self, new_name):
        self.full_widget_name = new_name # new name includes any type... + '_%s'%widget_type
        
        if self.has_OnClick:
            self.OnClick = self.full_widget_name + 'Click'
            
        if self.has_OnChange:
            self.OnChange = self.full_widget_name + 'Change'

        if self.Caption:
            self.Caption = self.full_widget_name
        
    
    def __init__(self, widget_type='Widget', label_text='',
                 widget_name='Generic', Left=0,  Height=25,  Top=0,  Width=80, 
                 TopMargin=6, RightMargin=6, BottomMargin=6, LeftMargin=6,
                 Caption=None, has_OnClick=True, has_OnChange=False,
                 has_OnSelectionChanged=False,
                 AutoSize=False, grow_for_long_text=True):
                 
        #self.base_widget_name = widget_name
        self.full_widget_name = make_legal_name( widget_name + '_%s'%widget_type)
        
        
        
        self.label_text = label_text
        
        self.widget_type = widget_type
        self.Left = Left
        self.Height = Height
        self.Top = Top
        self.Width = Width
        
        self.TopMargin = TopMargin
        self.RightMargin = RightMargin
        self.BottomMargin = BottomMargin
        self.LeftMargin = LeftMargin
        
        self.set_bbox()
        
        
        self.TabOrder = 0 # will be set later
        self.has_OnClick = has_OnClick
        self.has_OnChange = has_OnChange
        self.has_OnSelectionChanged = has_OnSelectionChanged
        
        self.AutoSize = AutoSize
        self.grow_for_long_text = grow_for_long_text
        
        if has_OnClick:
            self.OnClick = self.full_widget_name + '_Click'
        else:
            self.OnClick = None
        
        if has_OnChange:
            self.OnChange = self.full_widget_name + '_Change'
        else:
            self.OnChange = None
        
        if has_OnSelectionChanged:
            self.OnSelectionChanged = self.full_widget_name + '_SelectionChange'
        else:
            self.OnSelectionChanged = None


        if Caption is None:
            self.Caption = self.full_widget_name
        else:
            self.Caption = Caption
            
            
        if self.grow_for_long_text:
            for s in [label_text, self.Caption]:
                sugg_len = 10.0 + len(s) * 75.0 / 11.0
                if sugg_len > self.Width:
                    self.Width = int(sugg_len) + 1
            
        self.child_widgetL = [] # list of Widget objects owned by this widget
        self.indent = 0
        
    def set_indent(self, indent):
        self.indent = indent
    
    def get_full_widgetL(self):
        full_widgetL = [self]
        for child in self.child_widgetL:
            full_widgetL.extend( child.get_full_widgetL() )
        return full_widgetL

    
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

                     
    def set_bbox_upper_left(self, BBTop=10, BBLeft=10):
        self.Top = BBTop + self.TopMargin
        self.Left = BBLeft + self.LeftMargin
        self.set_bbox()

    
    def pas_var_define(self):
        sL = ['    %s: T%s;'%(self.full_widget_name, self.widget_type)  ]
        
        return '\n'.join(sL) #+ '\n'

    def pas_procedure_define(self):
        sL = []
        
        if self.has_OnClick:
            sL.append( '    procedure %s(Sender: TObject);'%self.OnClick )
        
        if self.has_OnChange:
            sL.append( '    procedure %s(Sender: TObject);'%self.OnChange )

        if self.has_OnSelectionChanged:
            sL.append( '    procedure %s(Sender: TObject);'%self.OnSelectionChanged )

        return '\n'.join(sL) #+ '\n'

    def pas_file_implement(self, form_name='Form1'):
        if not (self.has_OnClick or self.has_OnChange or self.has_OnSelectionChanged):
            return ''
        
        if self.has_OnClick:
            sL = ['procedure T%s.%s(Sender: TObject);'%(form_name, self.OnClick)  ]
            sL.append('begin')
            sL.append('    Last_Sender := Sender;')
            sL.append( "    %s.Caption := 'Clicked ' + Sender.ToString + ' %s';"%(form_name, self.OnClick) )
            sL.append('end;')

        # ============
        
        if self.has_OnChange:
            sL = ['procedure T%s.%s(Sender: TObject);'%(form_name, self.OnChange)  ]
            sL.append('begin')
            sL.append('    Last_Sender := Sender;')
            #sL.append( "    %s.Caption := 'Changed ' + Sender.ToString + ' %s';"%(form_name, self.OnChange) )
            sL.append( "    %s.Caption := 'Changed %s to ' + GetIOVarText(%s); "%(form_name, self.OnChange, self.full_widget_name) )
             
            sL.append('end;')
        
        # ============
        
        if self.has_OnSelectionChanged:
            sL = ['procedure T%s.%s(Sender: TObject);'%(form_name, self.OnSelectionChanged)  ]
            sL.append('begin')
            sL.append('    Last_Sender := Sender;')
            #sL.append( "    %s.Caption := 'Changed ' + Sender.ToString + ' %s';"%(form_name, self.OnChange) )
            sL.append( "    %s.Caption := 'Selection %s is ' + GetIOVarText(%s); "%(form_name, self.OnChange, self.full_widget_name) )
             
            sL.append('end;')

        return '\n'.join(sL) #+ '\n'

            
    def lfm_file_contents(self):
        """lfm files define form elements. Kind of a hierarchical config file."""
            
        pad = '  '*self.indent
        
        sL = [pad+'  object %s: T%s'%(self.full_widget_name, self.widget_type)  ]
        for s in ['Left','Height','Top','Width','AutoSize','Caption',
                  'OnClick','OnChange','OnSelectionChanged',
                  'TabOrder','Text',
                  'ClientHeight','ClientWidth',
                  'ActivePage','TabIndex']: # ActivePage and TabIndex used on PageControl & TabControl
            a = getattr(self, s, None)
            if not a is None:
                if s in ['Caption','Text']:
                    sL.append( pad+"    %s = '%s'"%(s,a) )
                else:
                    sL.append( pad+'    %s = %s'%(s,a) )
        
        for child in self.child_widgetL:
            child.set_indent( self.indent + 1 )
            sL.append( child.lfm_file_contents() )
                    
        sL.append(pad+'  end')
        sOut = '\n'.join(sL) + '\n'
        sOut = sOut.replace('\n\n','\n')
        return sOut


if __name__ == '__main__':
    
    F = Widget( widget_type='Button',
                widget_name='Generic', Left=41,  Height=25,  Top=42,  Width=75, 
                Caption=None, has_OnClick=True, has_OnChange=False)
                 
    print F.pas_var_define()
    print '='*55
    print F.pas_file_implement()
    print '='*55
    print F.lfm_file_contents()