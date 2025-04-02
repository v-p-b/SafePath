from safepath.path import WindowsPath 

def test_add_operator_string():
    p=WindowsPath()
    p += "Windows"
    p += "system32\\cmd.exe"
    assert str(p) == "C:\\Windows\\system32\\cmd.exe"

def test_drive_letter():
    p=WindowsPath()
    p.set_absolute("X:")
    p += "Windows"
    p += "system32\\cmd.exe"
    assert str(p) == "X:\\Windows\\system32\\cmd.exe"

def test_relative():
    p=WindowsPath()
    p.set_relative()
    p += "Windows"
    p += "system32\\cmd.exe"
    assert str(p) == "Windows\\system32\\cmd.exe"



def test_add_operator_list():
    p=WindowsPath()
    p += ["Windows", "system32", "cmd.exe"]
    assert str(p) == "C:\\Windows\\system32\\cmd.exe"

def test_add_operator_object():
    p1=WindowsPath()
    p2=WindowsPath()
    p1 += ["Windows", "system32"]
    p2 += "cmd.exe"
    p1 += p2
    assert str(p1) == "C:\\Windows\\system32\\cmd.exe"
