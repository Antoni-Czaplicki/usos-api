""" Example of fetching user data from the USOS API. """

import asyncio
import json
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
                verifier = input("Enter the PIN: ")
                await client.authorize(verifier)
                await client.save_access_token_to_file()

            user = await client.user_service.get_user()
            if user:
                print(user)
            else:
                print("User not found")

            groups = await client.group_service.get_groups_for_participant(
                ongoing_terms_only=True
            )
            print(groups)
            print(await client.helper.get_user_end_grades_with_weights())
    except USOSAPIException as e:
        print(f"Error fetching data: {e}")
    finally:
        if client:
            await client.close()


async def fetch_documentation(
    api_base_address: str, consumer_key: str, consumer_secret: str
):
    async with USOSClient(api_base_address, consumer_key, consumer_secret) as client:
        await client.load_access_token_from_file()
        documentation_service = client.api_documentation_service

        method_index = await documentation_service.get_method_index()
        modules = set()

        for method in method_index:
            module = method.name.split("/")[1]
            modules.add(module)

        modules_info = []
        for module in modules:
            print(f"Fetching documentation for module {module}")
            module_info = await documentation_service.get_module_info(module)
            module_info = module_info.dict()
            module_info["methods_info"] = {}
            for method in module_info["methods"]:
                print(f"Fetching documentation for method {method}")
                method_info = await documentation_service.get_method_info(method)
                module_info["methods_info"][method] = method_info.dict()

            modules_info.append(module_info)

    # Combine fetched data
    documentation = {
        "method_index": [method.dict() for method in method_index],
        "modules": [module for module in modules_info],
    }

    return documentation


async def save_documentation_to_file(file_path, documentation):
    with open(file_path, "w") as file:
        json.dump(documentation, file, indent=4)


if __name__ == "__main__":
    api_base_address = os.environ.get("USOS_API_BASE_ADDRESS", DEFAULT_API_BASE_ADDRESS)
    consumer_key = os.environ.get("USOS_CONSUMER_KEY")
    consumer_secret = os.environ.get("USOS_CONSUMER_SECRET")

    if not consumer_key or not consumer_secret:
        raise ValueError(
            "Consumer key and secret must be set in the environment variables."
        )

    asyncio.run(fetch_data(api_base_address, consumer_key, consumer_secret))
    # documentation = asyncio.run(fetch_documentation(api_base_address, consumer_key, consumer_secret))
    # asyncio.run(save_documentation_to_file("usos_api_documentation.json", documentation))
