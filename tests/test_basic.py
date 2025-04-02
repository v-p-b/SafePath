from safepath.path import Path 

def test_add_operator_string():
    p=Path()
    p += "etc"
    p += "ssh/sshd_config"
    assert str(p) == "/etc/ssh/sshd_config"

def test_add_operator_list():
    p=Path()
    p += ["etc", "ssh", "sshd_config"]
    assert str(p) == "/etc/ssh/sshd_config"

def test_add_operator_object():
    p1=Path()
    p2=Path()
    p1 += ["etc", "ssh"]
    p2 += "sshd_config"
    p1+=p2
    assert str(p1) == "/etc/ssh/sshd_config"
