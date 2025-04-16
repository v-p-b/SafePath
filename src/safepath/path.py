import re
from typing import Self, overload


class InvalidPathElementException(Exception):
    pass


class PathTraversalException(Exception):
    pass


class Path(object):
    def __init__(self, path: str = None) -> Self:
        self._elements = []
        self._separator = None
        self._element_regex = None
        self._relative_parents = None
        self._relative_currents = None
        self._root_element = None
        if isinstance(path, str):
           self.parse(path) 

    def _validate_relative_element(self, element: str):
        """Validates a single element that may be a relative element.
        Throws `InvalidPathElementException` if the element is invalid.

        Keyword arguments:
        element -- The element to validate.
        """
        m_element = self._element_regex.fullmatch(element)
        if m_element is None:
            raise InvalidPathElementException("Invalid character in element name")

    def _validate_element(self, element: str):
        """Validates a path element. The element must not be valid and non-relative.
        Throws `InvalidPathElementException` if the element is invalid.

        Keyword arguments:
        element -- The element to validate.
        """
        self._validate_relative_element(element)
        if self.is_parent_element(element) or self.is_current_element(element):
            raise InvalidPathElementException("Relative elements disallowed")

    def _validate_root(self, element: str):
        """Validates a root element.
        Should throw `InvalidPathElementException` if the element is invalid.
        Not implemented in the base class.

        Keyword arguments:
        element -- The element to validate.
        """
        raise NotImplementedError("Root validation not implemented in base class")

    def is_parent_element(self, element: str) -> bool:
        """Returns True if the element is relative, referencing the parent path. E.g.: '..'

        Keyword arguments:
        element -- The element to validate.
        """
        return element in self._relative_parents

    def is_current_element(self, element: str) -> bool:
        """Returns True if the element is relative, referencing the current path. E.g.: '.'

        Keyword arguments:
        element -- The element to validate.
        """
        return element in self._relative_currents

    def set_absolute(self, element: str) -> Self:
        """Sets a new root element, making the current path absolute.
        Throws `InvalidPathElementException` if the new root element is invalid.

        Keyword arguments:
        element -- The new root element.
        """
        self._validate_root(element)
        self._root_element = element
        return self

    def set_relative(self) -> Self:
        """Makes the path relative by unsetting the root element."""
        self._root_element = None
        return self

    def is_absolute(self) -> bool:
        """Returns true if the current path is an absolute path."""
        return self._root_element != None

    def __str__(self) -> str:
        """Returns the path as a string.
        Not implemented in the base class.
        """
        raise NotImplementedError("Not implemented in base class!")

    @overload
    def __add__(self, path: str) -> Self: ...

    @overload
    def __add__(self, path: list[str]) -> Self: ...

    @overload
    def __add__(self, path: Self) -> Self: ...

    @overload
    def __add__(self, path: list[str]) -> Self: ...

    def __add__(self, path) -> Self:
        """Appends a non-relative element to the path.
        Throws `InvalidPathElementException` if any path element is invalid.

        Keyword arguments:
        path -- The path segment to append. The argument can be a string, a list of elements (as strings) or a `Path` object.
        """
        if isinstance(path, str):
            self = self.parse_segment(path)
        elif isinstance(path, list):
            self = self.add_elements(path)
        elif isinstance(path, Path):
            self = self.add_elements(path.get_elements())
        else:
            raise NotImplementedError("Addition not implemented for this type")
        return self

    def __floordiv__(self, other) -> Self:
        return self.__add__(other)

    def __truediv__(self, other) -> Self:
        return self.__add__(other)

    def __sub__(self, levels: int) -> Self:
        """Traverses the current path toward the root for `levels` element.
        Throws `PathTraversalException` is the operation traverses beyond the last path element.

        Keyword arguments:
        levels -- An integer specifying the number of element to remove from the current path.
        """
        for _ in range(0, levels):
            try:
                self._elements.pop()
            except IndexError:
                raise PathTraversalException("Traversal beyond path root")
        return self

    def __contains__(self, item: Self) -> bool:
        """Returns True if `item` is a subpath of the current `Path` object."""
        item_elements = item.get_elements()
        for i, base_element in enumerate(self._elements):
            self._validate_element(base_element)
            if base_element != item_elements[i]:
                return False
        return True

    def get_elements(self) -> list[str]:
        """Returns a list of path elements that make up the current path."""
        return self._elements

    def add_elements(self, elements: list[str]) -> Self:
        """Adds a list of path elements to the current path.
        Throws `InvalidPathElementException` if any path element is invalid.
        """
        for e in elements:
            self._validate_element(e)
            self._elements.append(e)
        return self

    def parse(self, path: str) -> Self:
        """Parses a full path string into this Path object, replacing the previously represented path. The string must not contain relative elements.

        Keyword Arguments:
        path -- The path string to be parsed.
        """
        self._elements = []
        path_elements = path.split(self._separator)
        self.set_absolute(path_elements[0])
        self.add_elements(path_elements[1:])

        return self

    def parse_segment(self, path: str) -> Self:
        """Parses a string as a path segment and adds its elements to the current path. The path string must not be an absolute path.
        Throws `InvalidPathElementException` if any path element is invalid.
        """
        path_elements = path.split(self._separator)
        self.add_elements(path_elements)
        return self

    @overload
    def add_relative(self, path: str, base: str) -> Self: ...

    @overload
    def add_relative(self, path: str, base: Self) -> Self: ...

    def add_relative(self, path: str, base) -> Self:
        """Parses a path string into this Path object. The string can contain relative elements.
        TODO: Maybe this deserves an operator?

        Keyword Arguments:
        path -- The path string to be parsed.
        base -- The base directory represented as an absolute path string or Path object. If the resulting path is outside of this directory an exception is raised.
        """
        base_elements = None
        if isinstance(base, str):
            clazz = self.__class__
            base_elements = clazz().parse(base)
        elif isinstance(base, self.__class__):
            base_elements = base
        else:
            raise NotImplementedError("Parser not implemented for base path")

        for e in path.split(self._separator):
            self._validate_relative_element(e)
            if self.is_parent_element(e):
                self._elements.pop()  # Can raise IndexError
            elif not self.is_current_element(e):
                self._elements.append(e)

        if self not in base_elements:
            raise PathTraversalException("Traversal beyond base path")

        return self

    def _validate_root(self, element: str):
        """Validates a root element.
        Should throw `InvalidPathElementException` if the element is invalid.
        Not implemented in the base class.
        """
        raise NotImplementedError("Not implemented")


class UnixPath(Path):
    def __init__(self, path: str = None):
        super().__init__()
        self._elements = []
        self._separator = "/"
        self._element_regex = re.compile(r"[0-9A-Za-z-_\.]+")  # TODO
        self._relative_parents = [".."]
        self._relative_currents = [".", ""]
        self._root_element = ""
        if isinstance(path, str):
           self.parse(path) 

    def __str__(self) -> str:
        if self.is_absolute():
            return self._separator + self._separator.join(self._elements)
        else:
            return self._separator.join(self._elements)

    def _validate_root(self, element: str):
        if len(element) != 0:
            raise InvalidPathElementException("Invalid Unix root")


class WindowsPath(Path):
    _DRIVE_RE = re.compile("[A-Z]:")

    def __init__(self, path: str = None) -> Self:
        super().__init__()
        self._elements = []
        self._separator = "\\"
        self._element_regex = re.compile(r"[0-9A-Za-z-_\.]+")  # TODO
        self._relative_parents = [".."]
        self._relative_currents = [".", ""]
        self._root_element = "C:"
        if isinstance(path, str):
           self.parse(path) 

    def _validate_root(self, element: str):
        if WindowsPath._DRIVE_RE.fullmatch(element.upper()):
            return
        raise InvalidPathElementException("Invalid Windows drive root")

    def __str__(self) -> str:
        if self.is_absolute():
            return (
                self._root_element
                + self._separator
                + self._separator.join(self._elements)
            )
        else:
            return self._separator.join(self._elements)
