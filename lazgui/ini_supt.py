

INI_pasStrTypeD = {type(1):'Integer', type(1.23):'Float', 
               type('str'):'String', type(True):'Bool'}

def get_form_ini_proc_src(form_obj):
    """Generate the source for reading and writing INI files"""
    
    vname_typeL = sorted( zip(form_obj.widget_io_var_nameL, form_obj.widget_io_var_typeL, form_obj.widget_io_var_initL) )
    if len(vname_typeL) == 0:
        return ''
    
    len_max = max( [len(v[0]) for v in vname_typeL] )
    sfmt = "%" + '-%is'%len_max
    
    # start with the read procedure ====================================
    sL = ["""procedure read_from_file( fname: string);
var
    appINI : TIniFile;
begin
    
    appINI := TIniFile.Create( fname );
    
    try"""]

    # ======== Generate the Read statements
    for vname, vtype, vinit in vname_typeL:
        stype = INI_pasStrTypeD.get(vtype,'UNKNOWN')
        sL.append( "        %s := appINI.Read%s('Input', '%s', %s);"%(sfmt%vname, stype, vname, repr(vinit)) )


    # close the read procedure and open the save procedure ==============
    sL.append("""    finally
        appINI.Free;
    end;
    
end;

procedure save_to_file( fname: string);
var
    appINI : TIniFile;
begin
    
    appINI := TIniFile.Create( fname );
    
    try""")


    # ======== Generate the Write statements
    for vname, vtype, vinit in vname_typeL:
        stype = INI_pasStrTypeD.get(vtype,'UNKNOWN')
        sL.append( "        appINI.Write%s('Input', '%s', %s);"%( stype, vname, vname) )


    # close the save procedure ===========================================
    sL.append("""    finally
        appINI.Free;
    end;
    
end;
""")

    return '\n'.join(sL)