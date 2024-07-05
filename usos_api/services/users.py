from ..connection import USOSAPIConnection
from ..models.user import User


class UserService:
    def __init__(self, connection: USOSAPIConnection):
        self.connection = connection

    async def get_user(
        self, user_id: int | None = None, fields: list[str] | None = None
    ) -> User:
        """
        Get a user by their ID or the currently authorized user.

        :param user_id: The ID of the user to get. If None, the currently authorized user will be returned.
        :param fields: The fields to include in the response. Whole list of fields can be found `here <https://apps.usos.pwr.edu.pl/developers/api/services/users/#user>`_.
        :return: The user.
        """

        if fields is None:
            fields = [
                "id",
                "first_name",
                "last_name",
                "email",
                "student_number",
                "student_programmes",
                "student_status",
                "staff_status",
            ]  # Default fields
        fields = "|".join(fields)
        user_data = await self.connection.get(
            "services/users/user", user_id=user_id, fields=fields
        )
        return self._deserialize_user(user_data)

    def _deserialize_user(self, data: dict) -> User:
        return User(**data)
        # return User(
        #     id=data.get("id"),
        #     first_name=data.get("first_name"),
        #     middle_names=data.get("middle_names"),
        #     last_name=data.get("last_name"),
        #     previous_names=[
        #         PreviousName(
        #             first_name=pn.get("first_name"),
        #             last_name=pn.get("last_name"),
        #             until=pn.get("until"),
        #         )
        #         for pn in data.get("previous_names", [])
        #     ],
        #     sex=Sex(data.get("sex")) if data.get("sex") else None,
        #     titles=Title(
        #         before=data.get("titles", {}).get("before"),
        #         after=data.get("titles", {}).get("after"),
        #     ),
        #     student_status=(
        #         StudentStatus(data.get("student_status"))
        #         if data.get("student_status")
        #         else None
        #     ),
        #     staff_status=(
        #         StaffStatus(data.get("staff_status"))
        #         if data.get("staff_status")
        #         else None
        #     ),
        #     email_access=(
        #         EmailAccess(data.get("email_access"))
        #         if data.get("email_access")
        #         else None
        #     ),
        #     email=data.get("email"),
        #     email_url=data.get("email_url"),
        #     has_email=data.get("has_email"),
        #     homepage_url=data.get("homepage_url"),
        #     profile_url=data.get("profile_url"),
        #     phone_numbers=data.get("phone_numbers"),
        #     mobile_numbers=data.get("mobile_numbers"),
        #     office_hours=data.get("office_hours"),
        #     interests=data.get("interests"),
        #     has_photo=data.get("has_photo"),
        #     photo_urls=data.get("photo_urls", {}),
        #     student_number=data.get("student_number"),
        #     pesel=data.get("pesel"),
        #     birth_date=data.get("birth_date"),
        #     revenue_office_id=data.get("revenue_office_id"),
        #     citizenship=data.get("citizenship"),
        #     room=data.get("room"),
        #     student_programmes=[
        #         StudentProgramme(
        #             id=sp.get("id"),
        #             user=sp.get("user"),
        #             programme=sp.get("programme"),
        #             status=sp.get("status"),
        #             admission_date=sp.get("admission_date"),
        #             stages=sp.get("stages"),
        #             is_primary=sp.get("is_primary"),
        #         )
        #         for sp in data.get("student_programmes", [])
        #     ],
        #     employment_functions=[
        #         EmploymentFunction(
        #             function=ef.get("function"),
        #             faculty=ef.get("faculty"),
        #             is_official=ef.get("is_official"),
        #         )
        #         for ef in data.get("employment_functions", [])
        #     ],
        #     employment_positions=[
        #         EmploymentPosition(
        #             position=Position(
        #                 id=ep.get("position", {}).get("id"),
        #                 name=ep.get("position", {}).get("name"),
        #                 employment_group=ep.get("position", {}).get("employment_group"),
        #             ),
        #             faculty=ep.get("faculty"),
        #         ) for ep in data.get("employment_positions", [])
        #     ],
        #     course_editions_conducted=data.get("course_editions_conducted"),
        #     postal_addresses=[
        #         PostalAddress(
        #             type=pa.get("type"),
        #             type_name=pa.get("type_name"),
        #             address=pa.get("address"),
        #         ) for pa in data.get("postal_addresses", [])
        #     ],
        #     alt_email=data.get("alt_email"),
        #     can_i_debug=data.get("can_i_debug"),
        #     external_ids=(
        #         ExternalIds(
        #             orcid=data.get("external_ids", {}).get("orcid"),
        #             pbn_id=data.get("external_ids", {}).get("pbn_id"),
        #         )
        #     ),
        #     phd_student_status=data.get("phd_student_status"),
        #     library_card_id=data.get("library_card_id"),
        # )
