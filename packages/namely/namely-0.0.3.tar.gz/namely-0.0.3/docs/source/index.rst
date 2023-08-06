====================
Namely Python Client
====================


Non-official Python client for Namely_.

Learn more about Namely API here_.

.. _Namely: https://www.namely.com
.. _here: https://developers.namely.com/1.0/getting-started/introduction

Installation
------------

.. code-block:: shell

    pip install namely


Get started
-----------

.. code-block:: python

    # Import Namely API Client
    from namely import Client

    # Initialise Namely API Client
    client = Client("https://<your-domain>.namely.com/api/v1/", "<your-namely-api-token>")

    # Get all profiles
    get_all = client.profiles.get_all(multi_threading=False)

    # Get profile by Namely id
    person = client.profiles.get("<person-namely-id>")

    # Get my Namely profile
    me = client.profiles.get_me()

    # Get all profiles by filters
    mikes = client.profiles.filter(first_name="Mike")

    # Update profile by Namely id
    profile_to_update = {"user_status": "inactive"}
    updated_profile = client.profiles.update("<person-namely-id>", profile_to_update)

    # Create Namely profile
    new_profile = {
            "first_name": "John",
            "last_name": "Smith",
            "user_status": "active",
            "start_date": "2019-01-01",
            "email": "work@email.com"
            }
    created_profile = client.profiles.create(new_profile)

License
-------

`The MIT License`_

.. _The MIT License: license

.. toctree::
   :maxdepth: 3
   :caption: Resources

   profiles
