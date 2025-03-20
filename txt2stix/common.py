from typing import Any
from uuid import UUID

UUID_NAMESPACE = UUID("f92e15d9-6afc-5ae2-bb3e-85a1fd83a3b5")

class NamedDict(dict):
    def __getattribute__(self, attr: str):
        value = None
        try:
            value = super().__getattribute__(attr)
        except:
            pass
        if value is not None:
            return value
        return super().get(attr, "")

    def __setattr__(self, __name: str, __value: Any) -> None:
        return super().__setitem__(__name, __value)

class FatalException(Exception):
    pass
class MinorException(Exception):
    pass
