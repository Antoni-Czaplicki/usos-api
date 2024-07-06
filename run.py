""" Example of fetching user data from the USOS API. """

import asyncio
import os

from dotenv import load_dotenv

from usos_api.client import USOSClient
from usos_api.exceptions import USOSAPIException

load_dotenv()

DEFAULT_API_BASE_ADDRESS = "https://apps.usos.pwr.edu.pl/"


async def fetch_data(api_base_address: str, consumer_key: str, consumer_secret: str):
    try:
        async with USOSClient(
            api_base_address, consumer_key, consumer_secret
        ) as client:
            try:
                await client.load_access_token_from_file()
                await client.api_server_service.get_consumer_info()  # Check if the token is valid
            except:  # noqa
                print("No token found")
                print("Please visit the following URL to authorize the client:")
                client.set_scopes(["studies", "photo"])
                print(await client.get_authorization_url())
                token = input("Enter the PIN: ")
                await client.authorize(token)
                await client.save_access_token_to_file()

            user = await client.user_service.get_user()
            if user:
                fields = [
                    "id",
                    "first_name",
                    "middle_names",
                    "last_name",
                    "previous_names",
                    "sex",
                    "titles",
                    "student_status",
                    "staff_status",
                    "email_access",
                    "email",
                    "email_url",
                    "has_email",
                    "homepage_url",
                    "profile_url",
                    "phone_numbers",
                    "mobile_numbers",
                    "office_hours",
                    "interests",
                    "has_photo",
                    "photo_urls",
                    "student_number",
                    "pesel",
                    "birth_date",
                    "revenue_office_id",
                    "citizenship",
                    "room",
                    "student_programmes",
                    "employment_functions",
                    "employment_positions",
                    "course_editions_conducted",
                    "postal_addresses",
                    "alt_email",
                    "can_i_debug",
                    "external_ids",
                    "phd_student_status",
                    "library_card_id",
                ]
                for field in fields:
                    print(f"{field}: {getattr(user, field)}")
            else:
                print("User not found")

            groups = await client.group_service.get_groups_for_participant(
                ongoing_terms_only=True
            )
            print(groups)
    except USOSAPIException as e:
        print(f"Error fetching data: {e}")
    finally:
        if client:
            await client.close()


if __name__ == "__main__":
    api_base_address = os.environ.get("USOS_API_BASE_ADDRESS", DEFAULT_API_BASE_ADDRESS)
    consumer_key = os.environ.get("USOS_CONSUMER_KEY")
    consumer_secret = os.environ.get("USOS_CONSUMER_SECRET")

    if not consumer_key or not consumer_secret:
        raise ValueError(
            "Consumer key and secret must be set in the environment variables."
        )

    asyncio.run(fetch_data(api_base_address, consumer_key, consumer_secret))
