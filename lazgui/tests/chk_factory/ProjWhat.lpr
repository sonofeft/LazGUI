program ProjWhat;

{$mode objfpc}{$H+}

uses
  {$IFDEF UNIX}{$IFDEF UseCThreads}
  cthreads,
  {$ENDIF}{$ENDIF}
  Interfaces, // this includes the LCL widgetset
  Forms, MyForm1_Unit
  { you can add units after this };

{$R *.res}

begin
  RequireDerivedFormResource:=True;
  Application.Initialize;
  // Application.CreateForm(TForm1, Form1);
  Application.CreateForm(TMyForm1, MyForm1);
  Application.Run;
end.


