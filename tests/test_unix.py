import pytest
from safepath.path import UnixPath, WindowsPath


def test_add_operator_string():
    p = UnixPath()
    p += "etc"
    p += "ssh/sshd_config"
    assert str(p) == "/etc/ssh/sshd_config"


def test_relative():
    p = UnixPath()
    p = p.set_relative()
    p += "etc"
    p += "ssh/sshd_config"
    assert str(p) == "etc/ssh/sshd_config"


def test_relative_parse():
    p = UnixPath()
    p += ["var", "www", "app", "upload", "user1", "obj1"]
    p = p.add_relative("../obj2", "/var/www/app/upload/user1")
    assert str(p) == "/var/www/app/upload/user1/obj2"


def test_relative_parse_str():
    p = UnixPath()
    p += ["var", "www", "app", "upload", "user1", "obj1"]
    p = p.add_relative("../obj2", "/var/www/app/upload/user1")
    assert str(p) == "/var/www/app/upload/user1/obj2"


def test_relative_parse_obj():
    p = UnixPath()
    p += ["var", "www", "app", "upload", "user1", "obj1"]
    base = UnixPath()
    base += ["var", "www", "app", "upload", "user1"]
    p = p.add_relative("../obj2", base)
    assert str(p) == "/var/www/app/upload/user1/obj2"


def test_relative_parse_wrong_obj():
    p = UnixPath()
    p += ["var", "www", "app", "upload", "user1", "obj1"]
    base = WindowsPath()
    base += ["var", "www", "app", "upload", "user1"]
    with pytest.raises(Exception):
        p = p.add_relative("../obj2", base)


def test_relative_parse_too_deep():
    p = UnixPath()
    p += ["var", "www", "app", "upload", "user1", "obj1"]
    with pytest.raises(Exception):
        p = p.add_relative("../../obj2", "/var/www/app/upload/user1")


def test_add_operator_list():
    p = UnixPath()
    p += ["etc", "ssh", "sshd_config"]
    assert str(p) == "/etc/ssh/sshd_config"


def test_add_operator_object():
    p1 = UnixPath()
    p2 = UnixPath()
    p1 += ["etc", "ssh"]
    p2 += "sshd_config"
    p1 += p2
    assert str(p1) == "/etc/ssh/sshd_config"


def test_invalid():
    p = UnixPath()
    p += "etc"
    with pytest.raises(Exception):
        p += "?"


def test_invalid_relative():
    p = UnixPath()
    p += "etc"
    with pytest.raises(Exception):
        p += ".."


def test_invalid_relative2():
    p = UnixPath()
    p += "etc"
    with pytest.raises(Exception):
        p += "/passwd"


def test_invalid_relative3():
    p = UnixPath()
    p += "etc"
    with pytest.raises(Exception):
        p += "/../tmp"


def test_sub():
    p = UnixPath()
    p += "etc"
    p += "ssh"
    p -= 1
    assert str(p) == "/etc"


def test_sub_beyond_root():
    p = UnixPath()
    p += "etc"
    p += "ssh"
    with pytest.raises(Exception):
        p -= 3
