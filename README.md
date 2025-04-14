Safe Path
=========


**!!! EXPERIMENTAL CODE - DO NOT USE IN PRODUCTION !!!**

This is a prototype of a safe path handling library aimed to prevent directory traversal vulnerabilities.

Object Relational Mapping and Parameter Binding effectively reduced the density of SQL injection vulnerabilities. The idea is the same: prevent in-band singaling by eliminating string-based specification of filesystem paths, and provide an API that can separate control (relative paths, separator symbols) from data (file and directory names).

## Terminology

* Element - A file or directory in the path. E.g. `etc`, `system32`, `foo.txt`
  * Relative Element - An element that is a reference to either the current or the parent directory.
  * Root Element - An element that represents the root of a filesystem.
* Separator - A character that separates elements of a path. E.g. `/`, `\` 


## Principles

* Low friction - Development workflow should be close to simple string manipulation when handling valid inputs
  * This is achieved by chainable API's and operator overloading 
* Fail fast - Edge cases should be recognized early
  * Unexpected input results in exceptions
* Safety over Compatibility - Exotic filesystem features (e.g. Windows Device Paths, ADS's) should not be implemented to control complexity. Encountering such paths mean that a) edge cases should be handled at other parts of the system or b) a specialized, task-specific library is required.

## API Design

### Relative Paths 

Relative paths are special and users should explicitly request the handling of them:

* Overloaded operators don't accept Relative Elements
* Path objects never serialize to strings that contain Relative Elements
* Public methods only accept Relative Elements if this is indicated in the API name
* Public methods that accept Relative Elements always require the sepcification of a base path: if the final path is outside of the base path an exception is thrown
  * If during parsing of a path a Relative Element would traverse beyond the filesystem root, an exception is thrown


## Limitations

### Limited Portability

The library doesn't automatically handle the specifics of the filesystem of the runtime platform. One reason for this is security: to avoid confusion of symbols that have different meanings on different filesystems. The other reason is to support generating paths for remote filesystems where the expected format can't be determined based on the local enviroment.

Users must do OS detection if necessarry and instantiate the appropriate classes.

### Filesystems Only

Other locators (e.g. URL's) are not in scope of the library.

### Paths are Paths

The library doesn't provide information about whether a path exists, or about the filesystem object the path leads to (e.g. file vs. directory vs. symlink). This information should be obtained via OS-specific functions.


## TODO

* Documentation
* Proper exception types
* Atomicity: Guarantee that path operations either succeed or fail, and don't leave the object in an unpredictable state
* Thread safety?

