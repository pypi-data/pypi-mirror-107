# namely

Non-official Python client for [Namely](https://www.namely.com)

Learn more about Namely API [here](https://developers.namely.com/1.0/getting-started/introduction)

## Instalation

```bash
pip install namely
```

## Get started

```python
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
```

## License
The MIT License
