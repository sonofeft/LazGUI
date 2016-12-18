"""Represents a Form object in Lazarus"""
from laz_snippets import *
import ini_supt

pasStrTypeD = {type(1):'Integer', type(1.23):'Double', 
               type('str'):'String', type(True):'Boolean'}

class Form( object ):
    
    def __init__(self, form_name='Form1', layout=None, has_file_menu=True,
                 Left=611,  Height=240,  Top=162,  Width=320, 
                 Caption=None,  LCLVersion='1.6.0.4'):
        
        form_name = form_name.replace(' ','_')
        self.form_name = form_name
        #self.form_type_name = 'T'+form_name
        self.unit_name = form_name + '_Unit'
        
        self.has_file_menu = has_file_menu
        
        self.Left = Left
        self.Height = Height
        self.Top = Top
        self.Width = Width
        self.LCLVersion = LCLVersion
        self.widget_name_set = set() # used to prevent widgets with same name
        
        self.widget_io_var_nameL = [] # holds names of widget value variables
        self.var_widget_nameL = []    # holds names of widget
        self.widget_io_var_typeL = [] # holds types of widget value variables
        self.widget_io_var_initL = [] # holds initial value of widget value variables
        self.widget_io_full_widgetL = [] # holds the I/O widget objects themselves

        # may need to change ClientHeight and ClientWidth later.
        self.ClientHeight = Height
        self.ClientWidth = Width
        
        self.layout = layout
        if not layout is None:
            self.set_layout( layout )

        if Caption is None:
            self.Caption = form_name
        else:
            self.Caption = Caption
            
        self.laz_gui_obj = None
            
    def set_laz_gui_obj(self, laz_gui_obj):
        self.laz_gui_obj = laz_gui_obj
        
    def make_new_name(self, name):
        if name[-1].isdigit():
            c = int(name[-1])
        else:
            c = 1
        while name+str(c) in self.widget_name_set:
            c += 1
        return name+str(c)
        
    
    def set_layout(self, layout):
        #print 'Setting layout to WxH =',layout.ActualWidth,layout.ActualHeight
        self.layout = layout
        self.layout.set_indent( 0 )
        
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
        
        # check to make sure each widget's name is unique.  If not, change it.
        for widget in layout.get_full_widgetL():
            if not widget.full_widget_name in self.widget_name_set:
                self.widget_name_set.add( widget.full_widget_name )
            else:
                # change widgets name to unique name
                new_name = self.make_new_name( widget.full_widget_name )
                widget.change_full_name( new_name )
                self.widget_name_set.add( new_name )
            
            # if the widget has an I/O value, add it to the list of I/O-variable-widgets
            if hasattr(widget, 'value_type'):
                self.widget_io_var_nameL.append( widget.full_widget_name + '_val' ) # holds names of widget value variables
                self.var_widget_nameL.append( widget.full_widget_name ) # holds names of widget 
                self.widget_io_var_typeL.append( widget.value_type ) # holds types of widget value variables
                self.widget_io_var_initL.append( widget.initial_value ) # holds initial value of widget value variables
                self.widget_io_full_widgetL.append( widget )
        
        # If there are no I/O variables, don't make File Menu
        if len(self.widget_io_var_nameL)==0:
            self.has_file_menu = False
                
    
            
    def pas_file_contents(self):
        # use dictionary, D, to hold values for later string format statements
        if self.laz_gui_obj:
            D = {'project_name':self.laz_gui_obj.project_name}
        else:
            D = {'project_name':'ProjName'}
        
        # include all of self's properties in D's string format tasks
        D.update( self.__dict__ )
        
        # Get full widget list from layout
        full_widgetL = self.layout.get_full_widgetL()
        
        # create sL list to hold Form define widget variables
        sL = []
        for w in full_widgetL:
            sL.append( w.pas_var_define() )
            
        # as required, include history routines for file menu
        if self.has_file_menu:
            sL.append( PAS_HISTORY_VAR_DECLARATIONS )
            
        # use sL to create widget define entry into D
        D['widget_define_lines'] = '\n'.join(sL) #+ '\n'
        
        # start new sL list for form procedure define statements
        sL = []
        for w in full_widgetL:
            sL.append( w.pas_procedure_define() )      

        # if any of the widgets control an internal variable, inclide get/set procedure
        if len(self.widget_io_var_nameL) > 0:
            sL.append('    procedure Get_All_IO_Vars();')
            sL.append('    procedure Set_All_IO_Vars();')
            
        # as required, include history routines for file menu
        if self.has_file_menu:
            sL.append( PAS_HISTORY_PROC_DECLARATIONS )
        D['widget_define_procedures'] = '\n'.join(sL) #+ '\n'
        
        # Define global variables, including I/O Variables
        sL = []
        if self.has_file_menu:
            sL.append( "current_open_filename: string = '';" )
            sL.append( "  Version_Number: string = 'Version 1.0';" )
            
        # Add I/O variables to global variables
        if self.widget_io_var_nameL:
            sL.append('\n  // IO Variables')
        for vname, vtype, vinit in zip(self.widget_io_var_nameL, self.widget_io_var_typeL, self.widget_io_var_initL):
            stype = pasStrTypeD.get(vtype,'UNKNOWN')
            if vtype==type('str'): # string
                sL.append("  %s : %s = '%s';"%(vname, 'String', vinit))
            else:
                sL.append('  %s : %s = %s;'%(vname, stype, vinit))
        
        # use sL to make I/O variables D entry
        D['io_var_define'] = '\n'.join(sL)
        
        # start new sL list for implementation blocks
        sL = []
        
        # add INI file supt if required
        if self.has_file_menu:
            sL.append( ini_supt.get_form_ini_proc_src(self) ) # send self for access to props
        
        # Each widget may have an implementation section (OnClick, OnChange, etc.)
        for w in full_widgetL:
            s = w.pas_file_implement(form_name=self.form_name)
            if s:
                sL.append( s )
        
        # The get/set procedures for I/O variables (Get_All_IO_Vars and Set_All_IO_Vars) 
        if len(self.widget_io_var_nameL) > 0:
            sL.append('procedure T%s.Get_All_IO_Vars();'%self.form_name)
            sL.append('begin')
            for vname, wname, vtype, widget in zip(self.widget_io_var_nameL, self.var_widget_nameL, 
                                           self.widget_io_var_typeL, self.widget_io_full_widgetL):
                # sL.append('    %s := VarAsType(GetIOVarText(%s), var%s);'%(vname, wname, pasStrTypeD[vtype]) )
                
                if hasattr(widget,'label_text') and widget.label_text:
                    label = widget.label_text
                else:
                    label = widget.full_widget_name
                
                sL.append("    %s := GetIOVar%s(%s, %s, '%s');"%(vname, pasStrTypeD[vtype], wname, vname, label))
                
            sL.append('end;')
            
            sL.append('procedure T%s.Set_All_IO_Vars();'%self.form_name)
            sL.append('begin')
            for vname, wname, vtype in zip(self.widget_io_var_nameL, self.var_widget_nameL, self.widget_io_var_typeL):
                sL.append('    SetIOVarText(%s, VarToStr(%s));'%(wname, vname) )
            sL.append('end;')
        
        # as required, add menu history procedures to implementation
        if self.has_file_menu:
            sL.append( PAS_HISTORY_PROC_IMPLEMENTATION.format( **D ) )
        
        # create D entry for widget implementation
        D['widget_implementation_lines'] = '\n'.join(sL) #+ '\n'
        
        # finally, use D to format form *.pas file's template
        return PAS_FILE_TEMPLATE.format( **D )

            
    def lfm_file_contents(self):
        # use sL list to hold *.lfm lines for later concatenation
        sL = ['object %s: T%s'%(self.form_name, self.form_name)  ]
        
        # place form's properties into *.lfm file
        for s in ['Left','Height','Top','Width','Caption','LCLVersion','ClientHeight','ClientWidth']:
            a = getattr(self, s, False)
            if a:
                if s in ['Caption','LCLVersion']:
                    sL.append( "  %s = '%s'"%(s,a) )
                else:
                    sL.append( '  %s = %s'%(s,a) )

        # if there is a menu, the form needs these in *.lfm file
        if self.has_file_menu:
            sL.append( '  Menu = MainMenu1' )
            sL.append( '  OnCreate = FormCreate' )

        # Get full widget list from layout
        full_widgetL = self.layout.get_top_level_widgetL()
        
        # put all widgets in TabOrder
        itab = 0
        for w in full_widgetL:
            if hasattr(w, 'TabOrder'):
                w.TabOrder = itab
                itab += 1
            #if hasattr(w, 'TabOrder') or hasattr(w, 'Caption'):
            sL.append( w.lfm_file_contents() )
        
        # as required, put in menu history implementation
        if self.has_file_menu:
            sL.append( LFM_HISTORY_IMPLEMENTATION.format( **{'data_file_ext':'dat'} ) )
        
        
        sL.append('end')
        sOut = '\n'.join(sL) + '\n'
        sOut = sOut.replace('\n\n','\n')
        return sOut


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
    
    F = Form( form_name='MyForm1', layout=Lay,
              Left=611,  Height=240,  Top=162,  Width=320, 
              Caption='Quite the Fine Form',  LCLVersion='1.6.0.4')
                 

    #print F.lfm_file_contents()
    print '='*55
    print F.pas_file_contents()
    print '='*55
