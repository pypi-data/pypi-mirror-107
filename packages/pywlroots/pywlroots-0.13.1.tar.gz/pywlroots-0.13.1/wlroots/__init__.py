# Copyright (c) Sean Vig 2018

from typing import Any, Optional

from ._ffi import ffi, lib  # noqa: F401

__wlroots_version__ = "{}.{}.{}".format(
    lib.WLR_VERSION_MAJOR,
    lib.WLR_VERSION_MICRO,
    lib.WLR_VERSION_MINOR,
)

__version__ = "0.13.1"


class Ptr:
    """Add equality checks for objects holding the same cdata

    Objects that reference the same cdata objects will be treated as equal.
    Note that these objects will still have a different hash such that they
    should not collide in a set or dictionary.
    """

    _ptr: ffi.CData

    def __eq__(self, other) -> bool:
        """Return true if the other object holds the same cdata"""
        return hasattr(other, "_ptr") and self._ptr == other._ptr

    def __hash__(self) -> int:
        """Use the hash from `object`, which is unique per object"""
        return super().__hash__()


class PtrHasData(Ptr):
    """
    Add methods to get and set the void *data member on the wrapped struct. The value
    stored can be of any Python type.
    """

    @property
    def data(self) -> Optional[Any]:
        """Return any data that has been stored on the object"""
        if self._ptr.data == ffi.NULL:
            return None
        return ffi.from_handle(self._ptr.data)

    @data.setter
    def data(self, data: Any) -> None:
        """Store the given data on the current object"""
        self._data_handle = ffi.new_handle(data)
        self._ptr.data = self._data_handle
