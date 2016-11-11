unit MyForm1_Unit;

{$MODE Delphi}

interface

uses
  Classes, SysUtils, FileUtil, Forms, Controls, Graphics, 
  Dialogs, StdCtrls, ExtCtrls, Variants, get_set_io_var, 
  Menus, HistoryFiles, IniFiles, comctrls;

type

  { TMyForm1 }

  TMyForm1 = class(TForm)
    MyChoice_RadioGroup: TRadioGroup;
    Get_Text_Label: TLabel;
    Do_Wide_Things_Button: TButton;
    Get_What_Edit: TEdit;
    Get_Stuff_LabeledEdit: TLabeledEdit;
    MyPanel_Panel: TPanel;
    Get_Other_Stuff_LabeledEdit: TLabeledEdit;
    GetValueLabel_Label: TLabel;
    GetValue_Edit: TEdit;
    MyPageControl_PageControl: TPageControl;
    MyTabSheet_Panel: TTabSheet;
    Get_What_Edit1: TEdit;
    Get_Stuff_LabeledEdit1: TLabeledEdit;
    MyTabSheet_Panel1: TTabSheet;
    Get_What_Edit2: TEdit;
    Get_Stuff__2_LabeledEdit: TLabeledEdit;
    MyHistoryFiles: THistoryFiles;
    MainMenu1: TMainMenu;
    mnuFile: TMenuItem;
    mnuFileExit: TMenuItem;
    mnuFileOpen: TMenuItem;
    mnuFileReopen: TMenuItem;
    mnuFileSave: TMenuItem;
    OpenDialog1: TOpenDialog;
    SaveDialog1: TSaveDialog;  
    procedure MyChoice_RadioGroup_SelectionChange(Sender: TObject);

    procedure Do_Wide_Things_Button_Click(Sender: TObject);
    procedure Get_What_Edit_Change(Sender: TObject);
    procedure Get_Stuff_LabeledEdit_Change(Sender: TObject);

    procedure Get_Other_Stuff_LabeledEdit_Change(Sender: TObject);

    procedure GetValue_Edit_Change(Sender: TObject);


    procedure Get_What_Edit1Change(Sender: TObject);
    procedure Get_Stuff_LabeledEdit1Change(Sender: TObject);

    procedure Get_What_Edit2Change(Sender: TObject);
    procedure Get_Stuff__2_LabeledEdit_Change(Sender: TObject);
    procedure Get_All_IO_Vars();
    procedure Set_All_IO_Vars();
    procedure FormCreate(Sender: TObject);
    procedure mnuFileExitClick(Sender: TObject);
    procedure mnuFileSaveClick(Sender: TObject);
    procedure mnuFileOpenClick(Sender: TObject);
    procedure HistoryFilesClickHistoryItem(Sender: TObject;
      Item: TMenuItem; const Filename: String);
  private
    { private declarations }
  public
    { public declarations }
  end;

var
  MyForm1: TMyForm1;
  
  Last_Sender : TObject; // Used to stop "not used" Hints for Sender
  current_open_filename: string = '';
  Version_Number: string = 'Version 1.0';
  MyChoice_RadioGroup_val : String = 'default option #2';
  Get_What_Edit_val : String = 'No Label';
  Get_Stuff_LabeledEdit_val : String = 'Has Label';
  Get_Other_Stuff_LabeledEdit_val : String = 'LabeledEdit';
  GetValue_Edit_val : String = 'HLayout Wrapped';
  Get_What_Edit1_val : String = 'No Label';
  Get_Stuff_LabeledEdit1_val : String = 'Has Label';
  Get_What_Edit2_val : String = 'No Label #2';
  Get_Stuff__2_LabeledEdit_val : String = 'Has Label #2';

implementation

{$R *.lfm}

{ TMyForm1 }

procedure read_from_file( fname: string);
var
    appINI : TIniFile;
begin
    
    appINI := TIniFile.Create( fname );
    
    try
        GetValue_Edit_val               := appINI.ReadString('Input', 'GetValue_Edit_val', 'HLayout Wrapped');
        Get_Other_Stuff_LabeledEdit_val := appINI.ReadString('Input', 'Get_Other_Stuff_LabeledEdit_val', 'LabeledEdit');
        Get_Stuff_LabeledEdit1_val      := appINI.ReadString('Input', 'Get_Stuff_LabeledEdit1_val', 'Has Label');
        Get_Stuff_LabeledEdit_val       := appINI.ReadString('Input', 'Get_Stuff_LabeledEdit_val', 'Has Label');
        Get_Stuff__2_LabeledEdit_val    := appINI.ReadString('Input', 'Get_Stuff__2_LabeledEdit_val', 'Has Label #2');
        Get_What_Edit1_val              := appINI.ReadString('Input', 'Get_What_Edit1_val', 'No Label');
        Get_What_Edit2_val              := appINI.ReadString('Input', 'Get_What_Edit2_val', 'No Label #2');
        Get_What_Edit_val               := appINI.ReadString('Input', 'Get_What_Edit_val', 'No Label');
        MyChoice_RadioGroup_val         := appINI.ReadString('Input', 'MyChoice_RadioGroup_val', 'default option #2');
    finally
        appINI.Free;
    end;
    
end;

procedure save_to_file( fname: string);
var
    appINI : TIniFile;
begin
    
    appINI := TIniFile.Create( fname );
    
    try
        appINI.WriteString('Input', 'GetValue_Edit_val', GetValue_Edit_val);
        appINI.WriteString('Input', 'Get_Other_Stuff_LabeledEdit_val', Get_Other_Stuff_LabeledEdit_val);
        appINI.WriteString('Input', 'Get_Stuff_LabeledEdit1_val', Get_Stuff_LabeledEdit1_val);
        appINI.WriteString('Input', 'Get_Stuff_LabeledEdit_val', Get_Stuff_LabeledEdit_val);
        appINI.WriteString('Input', 'Get_Stuff__2_LabeledEdit_val', Get_Stuff__2_LabeledEdit_val);
        appINI.WriteString('Input', 'Get_What_Edit1_val', Get_What_Edit1_val);
        appINI.WriteString('Input', 'Get_What_Edit2_val', Get_What_Edit2_val);
        appINI.WriteString('Input', 'Get_What_Edit_val', Get_What_Edit_val);
        appINI.WriteString('Input', 'MyChoice_RadioGroup_val', MyChoice_RadioGroup_val);
    finally
        appINI.Free;
    end;
    
end;

procedure TMyForm1.MyChoice_RadioGroup_SelectionChange(Sender: TObject);
begin
    Last_Sender := Sender;
    MyForm1.Caption := 'Selection None is ' + GetIOVarText(MyChoice_RadioGroup); 
end;
procedure TMyForm1.Do_Wide_Things_Button_Click(Sender: TObject);
begin
    Last_Sender := Sender;
    MyForm1.Caption := 'Clicked ' + Sender.ToString + ' Do_Wide_Things_Button_Click';
end;
procedure TMyForm1.Get_What_Edit_Change(Sender: TObject);
begin
    Last_Sender := Sender;
    MyForm1.Caption := 'Changed Get_What_Edit_Change to ' + GetIOVarText(Get_What_Edit); 
end;
procedure TMyForm1.Get_Stuff_LabeledEdit_Change(Sender: TObject);
begin
    Last_Sender := Sender;
    MyForm1.Caption := 'Changed Get_Stuff_LabeledEdit_Change to ' + GetIOVarText(Get_Stuff_LabeledEdit); 
end;
procedure TMyForm1.Get_Other_Stuff_LabeledEdit_Change(Sender: TObject);
begin
    Last_Sender := Sender;
    MyForm1.Caption := 'Changed Get_Other_Stuff_LabeledEdit_Change to ' + GetIOVarText(Get_Other_Stuff_LabeledEdit); 
end;
procedure TMyForm1.GetValue_Edit_Change(Sender: TObject);
begin
    Last_Sender := Sender;
    MyForm1.Caption := 'Changed GetValue_Edit_Change to ' + GetIOVarText(GetValue_Edit); 
end;
procedure TMyForm1.Get_What_Edit1Change(Sender: TObject);
begin
    Last_Sender := Sender;
    MyForm1.Caption := 'Changed Get_What_Edit1Change to ' + GetIOVarText(Get_What_Edit1); 
end;
procedure TMyForm1.Get_Stuff_LabeledEdit1Change(Sender: TObject);
begin
    Last_Sender := Sender;
    MyForm1.Caption := 'Changed Get_Stuff_LabeledEdit1Change to ' + GetIOVarText(Get_Stuff_LabeledEdit1); 
end;
procedure TMyForm1.Get_What_Edit2Change(Sender: TObject);
begin
    Last_Sender := Sender;
    MyForm1.Caption := 'Changed Get_What_Edit2Change to ' + GetIOVarText(Get_What_Edit2); 
end;
procedure TMyForm1.Get_Stuff__2_LabeledEdit_Change(Sender: TObject);
begin
    Last_Sender := Sender;
    MyForm1.Caption := 'Changed Get_Stuff__2_LabeledEdit_Change to ' + GetIOVarText(Get_Stuff__2_LabeledEdit); 
end;
procedure TMyForm1.Get_All_IO_Vars();
begin
    MyChoice_RadioGroup_val := GetIOVarString(MyChoice_RadioGroup, MyChoice_RadioGroup_val, 'MyChoice_RadioGroup');
    Get_What_Edit_val := GetIOVarString(Get_What_Edit, Get_What_Edit_val, 'Get_What_Edit');
    Get_Stuff_LabeledEdit_val := GetIOVarString(Get_Stuff_LabeledEdit, Get_Stuff_LabeledEdit_val, 'Enter Stuff');
    Get_Other_Stuff_LabeledEdit_val := GetIOVarString(Get_Other_Stuff_LabeledEdit, Get_Other_Stuff_LabeledEdit_val, 'Enter Other Stuff');
    GetValue_Edit_val := GetIOVarString(GetValue_Edit, GetValue_Edit_val, 'GetValue_Edit');
    Get_What_Edit1_val := GetIOVarString(Get_What_Edit1, Get_What_Edit1_val, 'Get_What_Edit1');
    Get_Stuff_LabeledEdit1_val := GetIOVarString(Get_Stuff_LabeledEdit1, Get_Stuff_LabeledEdit1_val, 'Enter Stuff');
    Get_What_Edit2_val := GetIOVarString(Get_What_Edit2, Get_What_Edit2_val, 'Get_What_Edit2');
    Get_Stuff__2_LabeledEdit_val := GetIOVarString(Get_Stuff__2_LabeledEdit, Get_Stuff__2_LabeledEdit_val, 'Enter Stuff #2');
end;
procedure TMyForm1.Set_All_IO_Vars();
begin
    SetIOVarText(MyChoice_RadioGroup, VarToStr(MyChoice_RadioGroup_val));
    SetIOVarText(Get_What_Edit, VarToStr(Get_What_Edit_val));
    SetIOVarText(Get_Stuff_LabeledEdit, VarToStr(Get_Stuff_LabeledEdit_val));
    SetIOVarText(Get_Other_Stuff_LabeledEdit, VarToStr(Get_Other_Stuff_LabeledEdit_val));
    SetIOVarText(GetValue_Edit, VarToStr(GetValue_Edit_val));
    SetIOVarText(Get_What_Edit1, VarToStr(Get_What_Edit1_val));
    SetIOVarText(Get_Stuff_LabeledEdit1, VarToStr(Get_Stuff_LabeledEdit1_val));
    SetIOVarText(Get_What_Edit2, VarToStr(Get_What_Edit2_val));
    SetIOVarText(Get_Stuff__2_LabeledEdit, VarToStr(Get_Stuff__2_LabeledEdit_val));
end;
procedure TMyForm1.FormCreate(Sender: TObject);
var
  sPath : string;
begin
  MyForm1.Caption := Version_Number;

  MyHistoryFiles := THistoryFiles.Create(MyForm1);
  MyHistoryFiles.ParentMenu := mnuFileReopen;
  MyHistoryFiles.OnClickHistoryItem := MyForm1.HistoryFilesClickHistoryItem;
  MyHistoryFiles.MaxItems := 10;
  MyHistoryFiles.CheckLastItem := true;
  MyHistoryFiles.Position := 0;
  MyHistoryFiles.ShowFullPath:= false;

 // Store local path
  sPath := GetUserDir();
  MyHistoryFiles.LocalPath := sPath;

  // Define the ini filename and where it is.
  MyHistoryFiles.IniFile := sPath + 'ProjWhat.config';

  // Add the history on the parent menu
  MyHistoryFiles.UpdateParentMenu;

end;


procedure TMyForm1.mnuFileExitClick(Sender: TObject);
begin
  Close;
end;

procedure TMyForm1.mnuFileSaveClick(Sender: TObject);
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


procedure TMyForm1.mnuFileOpenClick(Sender: TObject);
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

procedure TMyForm1.HistoryFilesClickHistoryItem(Sender: TObject;
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



end.

