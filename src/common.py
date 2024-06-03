from typing import Any

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
class MinorExcption(Exception):
    pass