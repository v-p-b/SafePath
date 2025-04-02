from safepath.path import UnixPath 

def test_add_operator_string():
    p=UnixPath()
    p += "etc"
    p += "ssh/sshd_config"
    assert str(p) == "/etc/ssh/sshd_config"

def test_relative():
    p=UnixPath()
    p.set_relative()
    p += "etc"
    p += "ssh/sshd_config"
    assert str(p) == "etc/ssh/sshd_config"


def test_add_operator_list():
    p=UnixPath()
    p += ["etc", "ssh", "sshd_config"]
    assert str(p) == "/etc/ssh/sshd_config"

def test_add_operator_object():
    p1=UnixPath()
    p2=UnixPath()
    p1 += ["etc", "ssh"]
    p2 += "sshd_config"
    p1+=p2
    assert str(p1) == "/etc/ssh/sshd_config"
