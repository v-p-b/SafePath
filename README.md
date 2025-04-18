Safe Path
=========

**!!! EXPERIMENTAL CODE - DO NOT USE IN PRODUCTION !!!**

![example workflow](https://github.com/v-p-b/SafePath/actions/workflows/python-package.yml/badge.svg)

This is a prototype of a safe path handling library aimed to prevent directory traversal vulnerabilities.

Object Relational Mapping and Parameter Binding effectively reduced the density of SQL injection vulnerabilities. The idea is the same: prevent in-band singaling by eliminating string-based specification of filesystem paths, and provide an API that can separate control (relative paths, separator symbols) from data (file and directory names).


## Terminology

* Element - A file or directory in the path. E.g. `etc`, `system32`, `foo.txt`
  * Proper Element - An element that is neither a relative nor a root element. 
  * Relative Element - An element that is a reference to either the current or the parent directory.
  * Root Element - An element that represents the root of a filesystem.
* Separator - A character that separates elements of a path. E.g. `/`, `\`.
* Path Segment - Part of a path consisting of proper elements and their separator.
* Absolute Path - A path segment specifying a path from a root element. 


## Principles

* Low friction - Development workflow should be close to simple string manipulation when handling valid inputs
  * This is achieved by chainable API's and operator overloading 
* Fail fast - Edge cases should be recognized early
  * Unexpected input result in exceptions
* Safety over Compatibility - Exotic filesystem features (e.g. Windows Device Paths, ADS's) should not be implemented to control complexity. Encountering such paths mean that a) edge cases should be handled at other parts of the system or b) a specialized, task-specific library is required.


## API Design

API documentation can be generated with [pydoc](https://docs.python.org/3/library/pydoc.html). 

### Relative Paths 

Relative paths are special and users should explicitly request the handling of them:

* Overloaded operators don't accept Relative Elements
* Path objects never serialize to strings that contain Relative Elements
* Public methods only accept Relative Elements if this is indicated in the API name
* Public methods that accept Relative Elements always require the sepcification of a base path: if the final path is outside of the base path an exception is thrown
  * If during parsing of a path a Relative Element would traverse beyond the filesystem root, an exception is thrown

### Examples

From [tests](tests/), for now:

```py
def test_add_operator_string():
    p = UnixPath()
    p += "etc"
    p += "ssh/sshd_config"
    assert str(p) == "/etc/ssh/sshd_config"

def test_relative_parse():
    p = UnixPath()
    p += ["var", "www", "app", "upload", "user1", "obj1"]
    p = p.add_relative("../obj2", "/var/www/app/upload/user1")
    assert str(p) == "/var/www/app/upload/user1/obj2"

def test_invalid_relative():
    p = UnixPath()
    p += "etc"
    with pytest.raises(InvalidPathElementException):
        p += ".."


def test_relative_parse_too_deep():
    p = UnixPath()
    p += ["var", "www", "app", "upload", "user1", "obj1"]
    with pytest.raises(PathTraversalException):
        p = p.add_relative("../../obj2", "/var/www/app/upload/user1")

def test_drive_letter():
    p = WindowsPath()
    p.set_absolute("X:")
    p += "Windows"
    p += "system32\\cmd.exe"
    assert str(p) == "X:\\Windows\\system32\\cmd.exe"
```

## Limitations

### Limited Portability

The library doesn't automatically handle the specifics of the filesystem of the runtime platform. One reason for this is security: to avoid confusion of symbols that have different meanings on different filesystems. The other reason is to support generating paths for remote filesystems where the expected format can't be determined based on the local enviroment.

Users must perform OS detection if necessarry and instantiate the appropriate `Path` subclasses.

### Filesystems Only

Other locators (e.g. URL's) are not in scope of the library.

### Paths are Paths

The library doesn't provide information about whether a path exists, or about the filesystem object the path leads to (e.g. file vs. directory vs. symlink). This information should be obtained via OS-specific functions.


## Requirements

Python 3.11 is required. Otherwise the package should have no external dependencies.


## Usage

Being an experimental library, this package must only be used by implementing tests with [pytest](https://docs.pytest.org/en/stable/).

Installation in development mode: `pip install -e .`

Use the Issue Tracker liberally not only to report bugs and request features but also to suggest changes and even concerns about the overall design. 



## TODO

* More tests
* More documentation
* Proper element validation to match valid character sets on Windows and Unix-like systems
* Atomicity: Guarantee that path operations either succeed or fail, and don't leave the object in an unpredictable state
* Thread safety?

