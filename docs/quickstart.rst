Getting Started with USOS API
=============================

This page will guide you through the installation and basic usage of the USOS API package.

Installation
------------

The USOS API package can be installed using pip:

.. code-block:: bash

   pip install usos-api

Setting Up
----------

Before you can use the USOS API, you need to set up your API keys. These can be obtained from the USOS API website.
Remember that you need separate keys for each of the USOS serservers you want to access. You can find the list of available servers `here <https://apps.usos.edu.pl/developers/api/definitions/installations/>`_.

Preferred way of storing your API keys is to use environment variables. You can use the ``python-dotenv`` package to load them from a `.env` file. Here's an example of how to do it:

.. code-block:: python

   import os
   from dotenv import load_dotenv

   load_dotenv()

   api_base_address = os.environ.get("USOS_API_BASE_ADDRESS")
   consumer_key = os.environ.get("USOS_CONSUMER_KEY")
   consumer_secret = os.environ.get("USOS_CONSUMER_SECRET")

Technical info
--------------

The USOS API is asynchronous (using ``asyncio``) and works using
coroutines. All the code presented in this documentation needs to be placed
inside a coroutine block (except imports, obviously).

A sample coroutine block looks as follows:

.. code-block:: python

    import asyncio

    async def main():
        # asynchronous code goes here

    if __name__ == "__main__":
        asyncio.run(main())

Authentication
--------------

The USOS API uses OAuth 1.0a for authentication. The ``USOSClient`` class provides a method to authenticate with the USOS API. Here's an example of how to do it:

.. code-block:: python

   from usos_api.client import USOSClient

   async with USOSClient(api_base_address, consumer_key, consumer_secret) as client:
       print(await client.get_authorization_url()) # Open this URL in your browser, by default no callback URL is needed and you can just copy the PIN from the page you are redirected to
       verifier = input("Enter the PIN: ")
       await client.authorize(verifier)

Basic Usage
-----------

Here's a basic example of how to use the USOS API to fetch user data:

.. code-block:: python

   from usos_api.client import USOSClient

   async with USOSClient(api_base_address, consumer_key, consumer_secret) as client:
       load_access_token("access_token", "access_token_secret")
       user = await client.user_service.get_user()
       print(user)


You can also use the USOSClient without the context manager, but remember to close the client after you are done:

.. code-block:: python

   from usos_api.client import USOSClient

   client = USOSClient(api_base_address, consumer_key, consumer_secret)
   await client.open()
   load_access_token("access_token", "access_token_secret")
   user = await client.user_service.get_user()
   print(user)
   await client.close()


For more detailed usage, please refer to the full documentation.