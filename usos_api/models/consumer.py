from datetime import datetime

from pydantic import BaseModel


class Consumer(BaseModel):
    """
    Class representing a consumer.
    """

    name: str | None = None
    url: str | None = None
    email: str | None = None
    date_registered: datetime | None = None
    administrative_methods: list[str] | None = None
    token_scopes: list[str] | None = None
