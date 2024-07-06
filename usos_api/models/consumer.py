from datetime import datetime
from typing import List

from pydantic import BaseModel


class Consumer(BaseModel):
    """
    Class representing a consumer.
    """

    name: str | None = None
    url: str | None = None
    email: str | None = None
    date_registered: datetime | None = None
    administrative_methods: List[str] | None = None
    token_scopes: List[str] | None = None
