Safe Path
=========

## Terminology

* Element - A file or directory in the path. E.g. `etc`, `system32`, `foo.txt`
  * Relative Element - An element that is a reference to either the current or the parent directory.
  * Root Element - An element that references the root of a filesystem.
* Separator - A character that separates elements of a path. E.g. `/`, `\` 

## Principles

* Low friction - Development workflow should be close to simple string manipulation assuming valid inputs
  * This is achieved by chainable API's and operator overloading 
* Fail fast - Edge cases should be recognized early
  * Unexpected input results in exceptions

## Limitations

### Limited Portability

The library doesn't automatically handle the specifics of the target filesystem. One reason for this is security: to avoid confusion of symbols that have different meanings on different filesystems. The other reason is to support generating paths fore remote filesystems where the expected format can't be determined based on the local enviroment.

Users must do OS detection if necessarry and instantiate the appropriate classes.


### Filesystems Only

Other locators (e.g. URL's) are not in scope of the library.
