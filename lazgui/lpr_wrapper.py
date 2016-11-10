"""
Wraps the Lazarus *.lpr file that defines the project session.
Holds project_name, unit names, etc.
"""
import  sys

class LPR_File( object ):
    
    def __init__(self, project_name='project1', form1_name='Form1'):
        
        self.project_name = str(project_name)
        self.lpr_name = self.project_name + '.lpr'
        
        self.form_nameL = [ form1_name ]
        self.unit_nameL = [ form1_name + '_Unit' ]
        
        self.form_name_set = set( [form1_name.lower()] ) # save set of form names in lower case
                
    def add_form(self, new_form_name=None):
        
        if new_form_name is None:
            print "Need a valid new_form_name in lpi_wrapper"
            sys.exit()
            
        if new_form_name.lower() in self.form_name_set:
            print "Duplicate form names are NOT allowed in lpi_wrapper"
            sys.exit()
            
        self.form_name_set.add( new_form_name.lower() )
        self.form_nameL.append( new_form_name )
        self.unit_nameL.append( new_form_name + '_Unit' )
                    
    
    def file_contents(self):
        
        s = '  Application.CreateForm(T%s, %s);'
        L = [s%(name, name) for name in self.form_nameL]
        
        return LPR_TEMPLATE_STR % (self.project_name,  ', '.join(self.unit_nameL),  '\n'.join(L))
    
    def summ_print(self):
        print 'unit_nameL =',self.unit_nameL
        print self.file_contents()
        

LPR_TEMPLATE_STR = """program %s;

{$mode objfpc}{$H+}

uses
  {$IFDEF UNIX}{$IFDEF UseCThreads}
  cthreads,
  {$ENDIF}{$ENDIF}
  Interfaces, // this includes the LCL widgetset
  Forms, %s
  { you can add units after this };

{$R *.res}

begin
  RequireDerivedFormResource:=True;
  Application.Initialize;
  // Application.CreateForm(TForm1, Form1);
%s
  Application.Run;
end.


"""

if __name__ == "__main__":
    
    LPR = LPR_File(project_name='ChkProject', form1_name='ChkForm')
    LPR.add_form(new_form_name='XXXForm')
    LPR.add_form(new_form_name='ZZZForm')
    
    LPR.summ_print()
