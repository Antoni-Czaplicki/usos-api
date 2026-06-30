from typing import Annotated, Any

from pydantic import BeforeValidator


def usos_bool(value: Any) -> Any:
    if value is None or isinstance(value, bool):
        return value
    if isinstance(value, str):
        normalized = value.strip().upper()
        if normalized == "T":
            return True
        if normalized == "N":
            return False
    return value


USOSBool = Annotated[bool, BeforeValidator(usos_bool)]
