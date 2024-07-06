from datetime import datetime

from ..connection import USOSAPIConnection
from ..logger import get_logger
from ..models import Group, Term


def _filter_ongoing_terms(terms: list[Term]) -> list[Term]:
    """
    Filter out terms that are not ongoing.

    :param terms: The terms to filter.
    :return: The ongoing terms.
    """
    return [
        term
        for term in terms
        if term.start_date <= datetime.today().date() <= term.finish_date
    ]


def _deserialize_term(data: dict) -> Term:
    return Term(**data)


def _deserialize_group(data: dict, **kwargs) -> Group:
    data.update(kwargs)
    return Group(**data)


class GroupService:
    """
    A service for group-related operations.
    """

    def __init__(self, connection: USOSAPIConnection):
        """
        Initialize the group

        :param connection: The connection to use.
        """
        self.connection = connection
        self.logger = get_logger("GroupService")

    async def get_groups_by_ids(
        self, group_ids: list[tuple[str, int]], fields: list[str] = None
    ) -> list[Group]:
        """
        Get groups by their IDs.

        :param group_ids: The IDs of the groups to get. Each ID should be a tuple of course unit ID and group number.
        :param fields: The fields to include in the response.
        :return: A dictionary of group IDs to groups.
        """
        if not group_ids:
            return []
        if not fields:
            fields = ["course_unit_id", "group_number", "course_name"]
        if "course_unit_id" not in fields:
            fields.append("course_unit_id")
        if "group_number" not in fields:
            fields.append("group_number")
        fields = "|".join(fields)
        response = await self.connection.post(
            "services/groups/groups", group_id=group_ids, fields=fields
        )
        return [_deserialize_group(group) for group in response.values()]

    async def get_groups_for_lecturer(
        self,
        user_id: int | None = None,
        active_terms_only: bool = False,
        ongoing_terms_only: bool = False,
        fields: list[str] = None,
        lang: str = "en",
    ) -> list[Group]:
        """
        Get groups for a lecturer.

        :param user_id: The ID of the lecturer to get groups for, or None to get groups for the current user.
        :param active_terms_only: Whether to only get groups from active terms. Apparently, this parameter does not always work as expected, so you can use `ongoing_terms_only` instead.
        :param ongoing_terms_only: Whether to only get groups from ongoing terms (filtered locally based on start and finish dates).
        :param fields: The fields to include in the response.
        :param lang: Either pl or en - resulting list of groups will be sorted by the course name in the specified language.
        :return: A dictionary with the following fields: 'groups' (list of groups) and 'terms' (list of terms).
        """
        if not fields:
            fields = ["course_unit_id", "group_number", "course_name"]
        if "term_id" not in fields:
            fields.append("term_id")
        if active_terms_only and ongoing_terms_only:
            self.logger.warning(
                "Both active_terms_only and ongoing_terms_only are set to True. It is recommended to use only one of them."
            )
        fields = "|".join(fields)
        response = await self.connection.post(
            "services/groups/lecturer",
            user_id=user_id,
            active_terms=active_terms_only,
            fields=fields,
            lang=lang,
        )
        terms = [_deserialize_term(term) for term in response["terms"]]
        if ongoing_terms_only:
            terms = _filter_ongoing_terms(terms)
        term_ids = set(term.id for term in terms)
        return [
            _deserialize_group(group)
            for term_id, groups in response["groups"].items()
            if term_id in term_ids
            for group in groups
        ]

    async def get_groups_for_participant(
        self,
        user_id: int | None = None,
        active_terms_only: bool = False,
        ongoing_terms_only: bool = False,
        fields: list[str] = None,
        lang: str = "en",
    ) -> list[Group]:
        """
        Get groups for a participant.

        :param user_id: The ID of the participant to get groups for, or None to get groups for the current user.
        :param active_terms_only: Whether to only get groups from active terms. Apparently, this parameter does not always work as expected, so you can use `ongoing_terms_only` instead.
        :param ongoing_terms_only: Whether to only get groups from ongoing terms (filtered locally based on start and finish dates).
        :param fields: The fields to include in the response.
        :param lang: Either pl or en - resulting list of groups will be sorted by the course name in the specified language.
        :return: A dictionary with the following fields: 'groups' (list of groups) and 'terms' (list of terms).
        """
        if not fields:
            fields = ["course_unit_id", "group_number", "course_name", "term_id"]
        if "term_id" not in fields:
            fields.append("term_id")
        if active_terms_only and ongoing_terms_only:
            self.logger.warning(
                "Both active_terms_only and ongoing_terms_only are set to True. It is recommended to use only one of them."
            )
        fields = "|".join(fields)
        response = await self.connection.post(
            "services/groups/participant",
            user_id=user_id,
            active_terms=active_terms_only,
            fields=fields,
            lang=lang,
        )
        terms = [_deserialize_term(term) for term in response["terms"]]
        if ongoing_terms_only:
            terms = _filter_ongoing_terms(terms)
        term_ids = set(term.id for term in terms)
        return [
            _deserialize_group(group, term_id=term_id)
            for term_id, groups in response["groups"].items()
            if term_id in term_ids
            for group in groups
        ]

    async def get_groups_for_user(
        self,
        user_id: int | None = None,
        active_terms_only: bool = False,
        ongoing_terms_only: bool = False,
        fields: list[str] = None,
        lang: str = "en",
    ) -> list[Group]:
        """
        Get groups for a user.

        :param user_id: The ID of the user to get groups for, or None to get groups for the current user.
        :param active_terms_only: Whether to only get groups from active terms. Apparently, this parameter does not always work as expected, so you can use `ongoing_terms_only` instead.
        :param ongoing_terms_only: Whether to only get groups from ongoing terms (filtered locally based on start and finish dates).
        :param fields: The fields to include in the response.
        :param lang: Either pl or en - resulting list of groups will be sorted by the course name in the specified language.
        :return: A dictionary with the following fields: 'groups' (list of groups) and 'terms' (list of terms).
        """
        if not fields:
            fields = ["course_unit_id", "group_number", "course_name", "term_id"]
        if "term_id" not in fields:
            fields.append(
                "term_id"
            )  # We need term_id to filter out groups from terms that are not ongoing.
        if active_terms_only and ongoing_terms_only:
            self.logger.warning(
                "Both active_terms_only and ongoing_terms_only are set to True. It is recommended to use only one of them."
            )
        fields = "|".join(fields)
        response = await self.connection.post(
            "services/groups/user",
            user_id=user_id,
            active_terms=active_terms_only,
            fields=fields,
            lang=lang,
        )
        terms = [_deserialize_term(term) for term in response["terms"]]
        if ongoing_terms_only:
            terms = _filter_ongoing_terms(terms)
        term_ids = set(term.id for term in terms)
        return [
            _deserialize_group(group, term_id=term_id)
            for term_id, groups in response["groups"].items()
            if term_id in term_ids
            for group in groups
        ]
