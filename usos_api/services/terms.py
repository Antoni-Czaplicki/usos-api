from ..connection import USOSAPIConnection
from ..models import Term


class TermService:
    """
    A service for term-related operations.
    """

    def __init__(self, connection: USOSAPIConnection):
        """
        Initialize the term service.

        :param connection: The connection to use.
        """
        self.connection = connection

    async def get_term(self, term_id: str) -> Term:
        """
        Get a term by its ID.

        :param term_id: The ID of the term to get.
        :return: The term.
        """
        response = await self.connection.post("services/terms/term", term_id=term_id)
        return Term(**response)

    async def get_terms(self, term_ids: list[str]) -> list[Term]:
        """
        Get terms by their IDs.

        :param term_ids: The IDs of the terms to get, or a single term ID.
        :return: The terms.
        """

        term_ids = "|".join(term_ids)

        response = await self.connection.post("services/terms/terms", term_ids=term_ids)
        return [Term(**term) for term in response.values()]
