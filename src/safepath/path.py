import re
from typing import Self, overload


class Path(object):
    def __init__(self):
        self._elements = []
        self._separator = None
        self._element_regex = None
        self._relative_parents = None 
        self._relative_currents = None
        self._root_element = None

    def _validate_relative_element(self, element: str):
        m_element = self._element_regex.fullmatch(element)
        if m_element is None:
            raise Exception("Invalid character in element name")

    def _validate_element(self, element: str):
        self._validate_relative_element(element)
        if self.is_parent_element(element) or self.is_current_element(element):
            raise Exception("Relative elements disallowed")

    def _validate_root(self, element):
        raise NotImplementedError("Root validation not implemented in base class")

    def is_parent_element(self, e: str) -> bool:
        """Returns True if the element is relative, referencing the parent path. E.g.: '..'"""
        return e in self._relative_parents

    def is_current_element(self, element: str) -> bool:
        """Returns True if the element is relative, referencing the current path. E.g.: '.'"""
        return element in self._relative_currents

    def set_absolute(self, element: str):
        self._validate_root(element)
        self._root_element = element

    def set_relative(self):
        self._root_element = None

    def is_absolute(self):
        return self._root_element != None

    def __str__(self) -> str:
        """Returns the path as a string"""
        raise NotImplementedError("Not implemented in base class!")

    @overload
    def __add__(self, path: str) -> Self:
        """Appends a non-relative element to the path."""
        self.parse(path, True)
        return self

    @overload
    def __add__(self, path: str) -> Self:
        ...

    @overload
    def __add__(self, path: Self) -> Self:
        ...

    @overload
    def __add__(self, path: list[str]) -> Self:
        ...

    def __add__(self, path) -> Self:
        """Appends a non-relative element to the path."""
        if isinstance(path, str):
            self = self.parse(path, preserve=True)
        elif isinstance(path, list):
            self = self.add_elements(path)
        elif isinstance(path, Path):
            self = self.add_elements(path.get_elements())
        else:
            raise NotImplementedError("Addition not implemented for this type")
        return self

    def get_elements(self) -> list[str]:
        return self._elements

    def add_elements(self, elements: list[str]) -> Self:
        for e in elements:
            self._validate_element(e)
            self._elements.append(e)
        return self

    def parse(self, path: str, preserve: bool) -> Self:
        """Parses a path string into this Path object. The string must not contain relative elements.

        Keyword Arguments:
        path -- The path string to be parsed.
        preserve -- If True the path string will be appended to the existing path is this object. If False the path will be replaced.
        """
        if not preserve:
            self._elements = []
        for e in path.split(self._separator):
            self._validate_element(e)
            self._elements.append(e)
        return self

    def parse_relative(self, path: str, preserve: bool, base: list[str]) -> Self:
        """Parses a path string into this Path object. The string can contain relative elements.

        Keyword Arguments:
        path -- The path string to be parsed.
        preserve -- If True the path string will be appended to the existing path is this object. If False the path will be replaced.
        base -- The base directory represented as a list of valid elements. If the resulting path is outside of this directory an exception is raised.
        """

        if not preserve:
            self._elements = []
        for e in path.split(self._separator):
            self._validate_relative_element(e)
            if self.is_parent_element(e):
                self._elements.pop()  # Can raise IndexError
            if not self.is_current_element(e):
                self._elements.append(e)

        for i, base_element in enumerate(base):
            self._validate_element(base_element)
            if base_element != self._elements[i]:
                raise Exception("Traversal beyond base path")

        return self

    def _validate_root(self, element: str):
        raise NotImplementedError("Not implemented")

    def set_root(self, element: str) -> Self:
        _validate_root(element)
        self._root = element
        return self

class UnixPath(Path):
    def __init__(self):
        super().__init__()
        self._elements = []
        self._separator = "/"
        self._element_regex = re.compile(r"[0-9A-Za-z-_\.]+") # TODO
        self._relative_parents = [".."]
        self._relative_currents = [".", ""]
        self._root_element=""

    def __str__(self) -> str:
        if self.is_absolute():
            return self._separator+self._separator.join(self._elements)
        else:
            return self._separator.join(self._elements)

class WindowsPath(Path):
    _DRIVE_RE = re.compile("[A-Z]:")
    def __init__(self):
        super().__init__()
        self._elements = []
        self._separator = "\\"
        self._element_regex = re.compile(r"[0-9A-Za-z-_\.]+") # TODO
        self._relative_parents = [".."]
        self._relative_currents = [".", ""]
        self._root_element="C:"

    def _validate_root(self, element: str):
        if WindowsPath._DRIVE_RE.fullmatch(element.upper()):
            return
        raise Exception("Invalid Windows drive root")

    def __str__(self) -> str:
        if self.is_absolute():
            return self._root_element+self._separator+self._separator.join(self._elements)
        else:
            return self._separator.join(self._elements)

