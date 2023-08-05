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
    cl = Client("https://<your-domain>.namely.com/api/v1/", "<your-namely-api-token>")

    # Get all profiles
    get_all = cl.profiles.get_all()

    # Get profile by Namely id
    person = cl.profiles.get("<person-namely-id>")

    # Get all profiles by filters
    mikes = cl.profiles.filter(first_name="Mike")

License
-------

The MIT License
