; Voice-to-File AutoHotkey Controller
; Ctrl+LAlt: Toggle voice recognition (start/stop)

#Requires AutoHotkey v2.0

ScriptDir := A_ScriptDir
PythonScript := ScriptDir "\voice_to_file.py"

; Ctrl + Left Alt (toggle)
^<!:: {
    if !FileExist(PythonScript) {
        MsgBox("Python script not found: " PythonScript)
        return
    }

    RunWait('python "' PythonScript '"', , "Hide")
}
