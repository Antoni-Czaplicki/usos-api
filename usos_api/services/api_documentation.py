from usos_api.models.api_documentation import (
    APIMethodIndexItem,
    APIMethodInfo,
    APIModuleInfo,
    ScopeInfo,
)


class APIDocumentationService:
    """
    A service for API documentation fetching.
    """

    def __init__(self, connection):
        """
        Initialize the API documentation service.

        :param connection: The connection to use.
        """
        self.connection = connection

    async def get_method_info(
        self, method: str, fields: list[str] | None = None
    ) -> APIMethodInfo:
        """
        Get information about a specific method.

        :param method: The method to get information about.
        :param fields: The fields to include in the response.
        :return: Object representing the method.
        """

        if not method.startswith("services/"):
            method = f"services/{method}"

        response = await self.connection.post(
            "services/apiref/method", name=method, fields=fields
        )
        return APIMethodInfo(**response)

    async def get_method_index(self) -> list[APIMethodIndexItem]:
        """
        Get a list of API methods with brief descriptions.
        :return: List of objects representing the methods.
        """
        response = await self.connection.post("services/apiref/method_index")
        return [APIMethodIndexItem(**item) for item in response]

    async def get_module_info(self, module_name: str) -> APIModuleInfo:
        """
        Get information about a specific module.

        :param module_name: The name of the module.
        :return: Object representing the module.
        """
        if not module_name.startswith("services/"):
            module_name = f"services/{module_name}"
        response = await self.connection.post(
            "services/apiref/module", name=module_name
        )
        return APIModuleInfo(**response)

    async def get_scopes(self) -> list[ScopeInfo]:
        """
        Get a list of all scopes available in the USOS API installation.
        :return: List of scope information objects.
        """
        response = await self.connection.post("services/apiref/scopes")
        return [ScopeInfo(**scope) for scope in response]
