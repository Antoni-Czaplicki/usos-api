from typing import Any

from pydantic import BaseModel


class AuthOptions(BaseModel):
    consumer: str | None = None
    token: str | None = None
    administrative_only: bool | None = None
    ssl_required: bool | None = None


class Argument(BaseModel):
    name: str | None = None
    is_required: bool | None = None
    is_deprecated: bool | None = None
    default_value: Any | None = None
    description: str | None = None


class ResultField(BaseModel):
    name: str | None = None
    description: str | None = None
    is_primary: bool | None = None
    is_secondary: bool | None = None


class DeprecatedInfo(BaseModel):
    deprecated_by: str | None = None
    present_until: str | None = None


class APIMethodInfo(BaseModel):
    name: str | None = None
    short_name: str | None = None
    description: str | None = None
    brief_description: str | None = None
    ref_url: str | None = None
    auth_options: AuthOptions | None = None
    scopes: list[str] | None = None
    arguments: list[Argument] | None = None
    returns: str | None = None
    errors: str | None = None
    result_fields: list[ResultField] | None = None
    beta: bool | None = None
    deprecated: DeprecatedInfo | None = None
    admin_access: bool | None = None
    is_internal: bool | None = None


class APIMethodIndexItem(BaseModel):
    name: str | None = None
    brief_description: str | None = None


class APIModuleInfo(BaseModel):
    name: str | None = None
    title: str | None = None
    brief_description: str | None = None
    description: str | None = None
    submodules: list[str] | None = None
    methods: list[str] | None = None
    beta: bool | None = None


class ScopeInfo(BaseModel):
    key: str | None = None
    developers_description: str | None = None
