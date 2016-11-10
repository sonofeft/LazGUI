

PAS_FILE_TEMPLATE = """unit {unit_name};

{{$MODE Delphi}}

interface

uses
  Classes, SysUtils, FileUtil, Forms, Controls, Graphics, 
  Dialogs, StdCtrls, ExtCtrls, Variants, get_set_io_var, 
  Menus, HistoryFiles, IniFiles, comctrls;

type

  {{ T{form_name} }}

  T{form_name} = class(TForm)
{widget_define_lines}  
{widget_define_procedures}
  private
    {{ private declarations }}
  public
    {{ public declarations }}
  end;

var
  {form_name}: T{form_name};
  
  Last_Sender : TObject; // Used to stop "not used" Hints for Sender
  {io_var_define}

implementation

{{$R *.lfm}}

{{ T{form_name} }}

{widget_implementation_lines}

end.

"""

PAS_HISTORY_VAR_DECLARATIONS = """    MyHistoryFiles: THistoryFiles;
    MainMenu1: TMainMenu;
    mnuFile: TMenuItem;
    mnuFileExit: TMenuItem;
    mnuFileOpen: TMenuItem;
    mnuFileReopen: TMenuItem;
    mnuFileSave: TMenuItem;
    OpenDialog1: TOpenDialog;
    SaveDialog1: TSaveDialog;"""

PAS_HISTORY_PROC_DECLARATIONS = """    procedure FormCreate(Sender: TObject);
    procedure mnuFileExitClick(Sender: TObject);
    procedure mnuFileSaveClick(Sender: TObject);
    procedure mnuFileOpenClick(Sender: TObject);
    procedure HistoryFilesClickHistoryItem(Sender: TObject;
      Item: TMenuItem; const Filename: String);"""

PAS_HISTORY_PROC_IMPLEMENTATION = """procedure T{form_name}.FormCreate(Sender: TObject);
var
  sPath : string;
begin
  {form_name}.Caption := Version_Number;

  MyHistoryFiles := THistoryFiles.Create({form_name});
  MyHistoryFiles.ParentMenu := mnuFileReopen;
  MyHistoryFiles.OnClickHistoryItem := {form_name}.HistoryFilesClickHistoryItem;
  MyHistoryFiles.MaxItems := 10;
  MyHistoryFiles.CheckLastItem := true;
  MyHistoryFiles.Position := 0;
  MyHistoryFiles.ShowFullPath:= false;

 // Store local path
  sPath := GetUserDir();
  MyHistoryFiles.LocalPath := sPath;

  // Define the ini filename and where it is.
  MyHistoryFiles.IniFile := sPath + '{project_name}.config';

  // Add the history on the parent menu
  MyHistoryFiles.UpdateParentMenu;

end;


procedure T{form_name}.mnuFileExitClick(Sender: TObject);
begin
  Close;
end;

procedure T{form_name}.mnuFileSaveClick(Sender: TObject);
begin
  if SaveDialog1.Execute then
    begin
      Get_All_IO_Vars();
      save_to_file(SaveDialog1.Filename);
      MyHistoryFiles.UpdateList(SaveDialog1.FileName);
      self.Caption:= SaveDialog1.FileName;
      current_open_filename := SaveDialog1.FileName;
    end;
end;


procedure T{form_name}.mnuFileOpenClick(Sender: TObject);
begin
  with OpenDialog1 do
  begin
    if Execute then
    begin
      if FileName <> '' then
      begin
        // ShowMessage( 'Need to Open ' + FileName );
        read_from_file( FileName );
        Set_All_IO_Vars();
        self.Caption:= FileName;
        current_open_filename := FileName;

        // Add the filename into the history and refresh the menu
        MyHistoryFiles.UpdateList(FileName);
      end;
    end;
  end;
end;

procedure T{form_name}.HistoryFilesClickHistoryItem(Sender: TObject;
  Item: TMenuItem; const Filename: String);
begin
  MyHistoryFiles.UpdateList(FileName);
  MyHistoryFiles.UpdateParentMenu;
  // When an Item is clicked the file is loaded on the Memo
  // ShowMessage( 'Need to Open ' + FileName );
  read_from_file( FileName );
  Set_All_IO_Vars();
  self.Caption:= FileName;
  current_open_filename := FileName;
end;

"""

LFM_HISTORY_IMPLEMENTATION = """  object MainMenu1: TMainMenu
    left = 8
    top = 8
    object mnuFile: TMenuItem
      Caption = '&File'
      object mnuFileOpen: TMenuItem
        Caption = '&Open'
        OnClick = mnuFileOpenClick
      end
      object mnuFileReopen: TMenuItem
        Caption = '&ReOpen'
      end
      object mnuFileSave: TMenuItem
        Caption = '&Save'
        OnClick = mnuFileSaveClick
      end
      object mnuFileExit: TMenuItem
        Caption = '&Exit'
        OnClick = mnuFileExitClick
      end
    end
  end
  object OpenDialog1: TOpenDialog
    Filter = 'Input File|*.{data_file_ext}'
    left = 16
    top = 558
  end
  object SaveDialog1: TSaveDialog
    Filter = 'Input File|*.{data_file_ext}'
    Options = [ofOverwritePrompt, ofEnableSizing, ofViewDetail]
    left = 88
    top = 558
  end
"""

