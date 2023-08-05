"""Module for `profiles` resource"""
import logging
from concurrent.futures import ThreadPoolExecutor
from typing import Dict

from retrying import retry

from .._config import STOP_MAX_ATTEMPT_NUMBER, WAIT_FIXED
from .helpers import BaseResource


class Profile(BaseResource):
    """
    A class used to operate `profiles` resource

    ...

    Methods
    -------
    get_all(limit: int = 50)
        Returns all Namely profiles
    get(_id: str)
        Returns a Namely profile by profile id
    get_me()
        Returns current user's Namely profile
    filter(
        first_name: str = None,
        last_name: str = None,
        email: str = None,
        personal_email: str = None,
        job_title: str = None,
        reports_to: str = None,
        user_status: str = None,
        limit: int = 50,
    )
        Returns all Namely profiles with applied filters
    update(id: str, profile: Dict)
        Updates Namely profile by id
    create(profile: Dict)
        Creates a new Namely profile
    """

    @retry(stop_max_attempt_number=STOP_MAX_ATTEMPT_NUMBER, wait_fixed=WAIT_FIXED)
    def get_all(self, limit: int = 50) -> Dict:
        """
        Returns all Namely profiles sending multiple requests in multiple threads

        Parameters
        ----------
        limit : int, default value is 50
            Number of profiles to get from Namely per request.
            Note: this method returns all profiles with all fields based on user permissions

        See Also
        --------
        Profile.get : method to get profile by Namely id.
        Profile.me : method to get current user's profile.
        Profile.filter : method to get filtered profiles.

        Examples
        --------
        Using `get_all` method.

        >>> from namely import Client
        >>> client = Client("https://your-company.namely/api/v1/", "your-namely-api-token")
        >>> me = client.profiles.get_all(limit=10)
        >>> me
        {
            "profiles": [
                {
                    "id": "namely-profile-id",
                    "company_uuid": "109fbc88-8cac-45fb-bddb-ebd0d5a8c0b4",
                    "email": "john.doe@your-company.com",
                    "first_name": "John",
                    "last_name": "Doe",
                    "user_status": "active",
                    "preferred_name": "Jo",
                    ""full_name": "Jo Doe",
                    "job_title": {
                        "id": "3be1c271-2be0-459d-b587-d2911354dbca",
                        "title": "Chief Executife Officer"
                    },
                    "links": {
                        "job_title": {
                            "id": "3be1c271-2be0-459d-b587-d2911354dbca",
                            "title": "Chief Executife Officer"
                        },
                        "groups": [
                            {
                                "id": "c2bad067-6f48-4a4b-8b25-06c16bebc145",
                                "name": "Your Company"
                            },
                        ],
                        "teams": []
                    },
                    ...
                },
                ...
            ],
            "meta": {
                "count": 1,
                "status": 200,
                "total_count": 1
            },
            "links": {
                "profiles.job_title": {
                    "type": "job_titles"
                },
                "profiles.image": {
                    "type": "files"
                },
                "profiles.groups": {
                    "type": "groups"
                },
                "profiles.teams": {
                    "type": "teams"
                }
            },
            "linked": {
                "job_titles": [
                    {
                        "id": "3be1c271-2be0-459d-b587-d2911354dbca",
                        "parent_id": "853e4a3c-a9c3-4f38-8f79-3aa9b80e1266",
                        "title": "Chief Executife Officer",
                        "links": {
                            "job_tier": "853e4a3c-a9c3-4f38-8f79-3aa9b80e1266"
                        },
                        "active": true
                    },
                    ...
                ],
                "files": [],
                "groups": [
                    {
                        "id": "c2bad067-6f48-4a4b-8b25-06c16bebc145",
                        "title": "Your Company",
                        "type": "Subsidiary",
                        "is_team": true,
                        "address": null,
                        "count": 0,
                        "links": {
                            "group_type": "1ab11dab-c4eb-45ab-1be2-dbed5a1f5f1e"
                        }
                    },
                    ...
                ],
                "teams": []
            }
        }

        Raises
        ------
        EntityNotFound - when response status code is 404
        AccessDenied - when response status code is 403
        RequestError - when response status code is other 400 error
        """

        logging.info("Starting getting all profiles from Namely")
        all_profiles = []
        path = "profiles.json?page={}&per_page={}"
        response = self._get_json(path.format(1, 2))
        total_count = response["meta"]["total_count"]
        logging.info(f"There is {total_count} profiles")

        pages = range(1, (total_count // limit) + 2)
        futures = []
        links = response["links"]
        linked = {
            "job_titles": [],
            "files": [],
            "groups": [],
            "teams": [],
        }
        job_titles_added, groups_added, files_added, teams = {}, {}, {}, {}
        with ThreadPoolExecutor() as executor:
            for page in pages:
                future = executor.submit(self._get_json, path.format(page, limit))
                futures.append(future)
        for future in futures:
            try:
                result = future.result()
            except Exception as err:
                logging.exception(
                    "Exception in ThreadPoolExecutor",
                    extra={"extra": {"error": str(err)}},
                )
            else:
                if result and result.get("profiles"):
                    all_profiles.extend(result["profiles"])
                    linked["job_titles"].extend(
                        [
                            job_title
                            for job_title in result["linked"]["job_titles"]
                            if not job_titles_added.get(job_title["id"])
                        ]
                    )
                    job_titles_added.update(
                        {job_title["id"]: None for job_title in result["linked"]["job_titles"]}
                    )
                    linked["groups"].extend(
                        [
                            group
                            for group in result["linked"]["groups"]
                            if not groups_added.get(group["id"])
                        ]
                    )
                    groups_added.update({group["id"]: None for group in result["linked"]["groups"]})
                    linked["files"].extend(
                        [
                            file
                            for file in result["linked"]["files"]
                            if not files_added.get(file["id"])
                        ]
                    )
                    files_added.update({file["id"]: None for file in result["linked"]["files"]})
                    linked["teams"].extend(
                        [team for team in result["linked"]["teams"] if not teams.get(team["id"])]
                    )
                    teams.update({team["id"]: None for team in result["linked"]["teams"]})
        logging.info(f"Returning {len(all_profiles)} profiles")
        return {
            "profiles": all_profiles,
            "meta": {"total_count": total_count},
            "links": links,
            "linked": linked,
        }

    @retry(stop_max_attempt_number=STOP_MAX_ATTEMPT_NUMBER, wait_fixed=WAIT_FIXED)
    def get(self, _id: str) -> Dict:
        """
        Returns a Namely profile by Namely profile id

        Parameters
        ----------
        _id : str
            Namely profile id.
            Example: `051f9e32-4365-4ad3-a60f-572a76a41ce1`

        See Also
        --------
        Profile.me : method to get current user's profile.
        Profile.get_all : method to get all profiles.
        Profile.filter : method to get filtered profiles.

        Examples
        --------
        Using `get` method.

        >>> from namely import Client
        >>> client = Client("https://your-company.namely/api/v1/", "your-namely-api-token")
        >>> profile = client.profiles.get("namely-profile-id")
        >>> profile
        {
            "profiles": [
                {
                    "id": "namely-profile-id",
                    "company_uuid": "109fbc88-8cac-45fb-bddb-ebd0d5a8c0b4",
                    "email": "john.doe@your-company.com",
                    "first_name": "John",
                    "last_name": "Doe",
                    "user_status": "active",
                    "preferred_name": "Jo",
                    ""full_name": "Jo Doe",
                    "job_title": {
                        "id": "3be1c271-2be0-459d-b587-d2911354dbca",
                        "title": "Chief Executife Officer"
                    },
                    "links": {
                        "job_title": {
                            "id": "3be1c271-2be0-459d-b587-d2911354dbca",
                            "title": "Chief Executife Officer"
                        },
                        "groups": [
                            {
                                "id": "c2bad067-6f48-4a4b-8b25-06c16bebc145",
                                "name": "Your Company"
                            },
                        ],
                        "teams": []
                    },
                }
            ],
            "meta": {
                "count": 1,
                "status": 200,
                "total_count": 1
            },
            "links": {
                "profiles.job_title": {
                    "type": "job_titles"
                },
                "profiles.image": {
                    "type": "files"
                },
                "profiles.groups": {
                    "type": "groups"
                },
                "profiles.teams": {
                    "type": "teams"
                }
            },
            "linked": {
                "job_titles": [
                    {
                        "id": "3be1c271-2be0-459d-b587-d2911354dbca",
                        "parent_id": "853e4a3c-a9c3-4f38-8f79-3aa9b80e1266",
                        "title": "Chief Executife Officer",
                        "links": {
                            "job_tier": "853e4a3c-a9c3-4f38-8f79-3aa9b80e1266"
                        },
                        "active": true
                    },
                    ...
                ],
                "files": [],
                "groups": [
                    {
                        "id": "c2bad067-6f48-4a4b-8b25-06c16bebc145",
                        "title": "Your Company",
                        "type": "Subsidiary",
                        "is_team": true,
                        "address": null,
                        "count": 0,
                        "links": {
                            "group_type": "1ab11dab-c4eb-45ab-1be2-dbed5a1f5f1e"
                        }
                    },
                    ...
                ],
                "teams": []
            }
        }

        Raises
        ------
        EntityNotFound - when response status code is 404
        AccessDenied - when response status code is 403
        RequestError - when response status code is other 400 error
        """

        logging.info("Starting getting Namely profile by id")
        return self._get_json(f"profiles/{_id}.json")

    @retry(stop_max_attempt_number=STOP_MAX_ATTEMPT_NUMBER, wait_fixed=WAIT_FIXED)
    def get_me(self) -> Dict:
        """
        Returns current user's Namely profile

        See Also
        --------
        Profile.get : method to get profile by Namely id.
        Profile.get_all : method to get all profiles.
        Profile.filter : method to get filtered profiles.

        Examples
        --------
        Using `get_me` method.

        >>> from namely import Client
        >>> client = Client("https://your-company.namely/api/v1/", "your-namely-api-token")
        >>> me = client.profiles.get_me()
        >>> me
        {
            "profiles": [
                {
                    "id": "namely-profile-id",
                    "company_uuid": "109fbc88-8cac-45fb-bddb-ebd0d5a8c0b4",
                    "email": "john.doe@your-company.com",
                    "first_name": "John",
                    "last_name": "Doe",
                    "user_status": "active",
                    "preferred_name": "Jo",
                    ""full_name": "Jo Doe",
                    "job_title": {
                        "id": "3be1c271-2be0-459d-b587-d2911354dbca",
                        "title": "Chief Executife Officer"
                    },
                    "links": {
                        "job_title": {
                            "id": "3be1c271-2be0-459d-b587-d2911354dbca",
                            "title": "Chief Executife Officer"
                        },
                        "groups": [
                            {
                                "id": "c2bad067-6f48-4a4b-8b25-06c16bebc145",
                                "name": "Your Company"
                            },
                        ],
                        "teams": []
                    },
                }
            ],
            "meta": {
                "count": 1,
                "status": 200,
                "total_count": 1
            },
            "links": {
                "profiles.job_title": {
                    "type": "job_titles"
                },
                "profiles.image": {
                    "type": "files"
                },
                "profiles.groups": {
                    "type": "groups"
                },
                "profiles.teams": {
                    "type": "teams"
                }
            },
            "linked": {
                "job_titles": [
                    {
                        "id": "3be1c271-2be0-459d-b587-d2911354dbca",
                        "parent_id": "853e4a3c-a9c3-4f38-8f79-3aa9b80e1266",
                        "title": "Chief Executife Officer",
                        "links": {
                            "job_tier": "853e4a3c-a9c3-4f38-8f79-3aa9b80e1266"
                        },
                        "active": true
                    },
                    ...
                ],
                "files": [],
                "groups": [
                    {
                        "id": "c2bad067-6f48-4a4b-8b25-06c16bebc145",
                        "title": "Your Company",
                        "type": "Subsidiary",
                        "is_team": true,
                        "address": null,
                        "count": 0,
                        "links": {
                            "group_type": "1ab11dab-c4eb-45ab-1be2-dbed5a1f5f1e"
                        }
                    },
                    ...
                ],
                "teams": []
            }
        }

        Raises
        ------
        EntityNotFound - when response status code is 404
        AccessDenied - when response status code is 403
        RequestError - when response status code is other 400 error
        """

        logging.info("Starting getting Namely profile by id")
        return self._get_json("profiles/me.json")

    @retry(stop_max_attempt_number=STOP_MAX_ATTEMPT_NUMBER, wait_fixed=WAIT_FIXED)
    def filter(
        self,
        first_name: str = None,
        last_name: str = None,
        email: str = None,
        personal_email: str = None,
        job_title: str = None,
        reports_to: str = None,
        user_status: str = None,
        limit: int = 50,
    ) -> Dict:
        """
        Returns all Namely profiles with applied filters sending
        multiple requests in multiple threads

        Parameters
        ----------
        first_name: str, optional, default value is `None`
            Employees `first_name`, for example `John`
        last_name: str, optional, default value is `None`
            Employees `last_name`, for example `Doe`
        email: str, optional, default value is `None`
            Employees company email, for example `john.doe@your-company.com`
        personal_email: str, optional, default value is `None`
            Employees personal email, for example `john.doe@email.com`
        job_title: str, optional, default value is `None`
            Employees `job_title`, for example `HR Admin`
        reports_to: str, optional, default value is `None`
            Employees `reports_to` (manager) Namely id,
            for example `8be1c671-2be4-452d-b587-d2711354dbcc`
        user_status: str, optional, default value is `None`
            Employees `user_status`, can be one of the options: `active`, `inactive`, `pending`
        limit : int, default value is `50`
            Number of profiles to get from Namely per request.
            Note: this method returns all profiles with all fields based on user permissions

        See Also
        --------
        Profile.get : method to get profile by Namely id.
        Profile.me : method to get current user's profile.
        Profile.filter : method to get filtered profiles.

        Examples
        --------
        Using `get_all` method.

        >>> from namely import Client
        >>> client = Client("https://your-company.namely/api/v1/", "your-namely-api-token")
        >>> me = client.profiles.filter(limit=10)
        >>> me
        {
            "profiles": [
                {
                    "id": "namely-profile-id",
                    "company_uuid": "109fbc88-8cac-45fb-bddb-ebd0d5a8c0b4",
                    "email": "john.doe@your-company.com",
                    "first_name": "John",
                    "last_name": "Doe",
                    "user_status": "active",
                    "preferred_name": "Jo",
                    ""full_name": "Jo Doe",
                    "job_title": {
                        "id": "3be1c271-2be0-459d-b587-d2911354dbca",
                        "title": "Chief Executife Officer"
                    },
                    "links": {
                        "job_title": {
                            "id": "3be1c271-2be0-459d-b587-d2911354dbca",
                            "title": "Chief Executife Officer"
                        },
                        "groups": [
                            {
                                "id": "c2bad067-6f48-4a4b-8b25-06c16bebc145",
                                "name": "Your Company"
                            },
                        ],
                        "teams": []
                    },
                    ...
                },
                ...
            ],
            "meta": {
                "count": 1,
                "status": 200,
                "total_count": 1
            },
            "links": {
                "profiles.job_title": {
                    "type": "job_titles"
                },
                "profiles.image": {
                    "type": "files"
                },
                "profiles.groups": {
                    "type": "groups"
                },
                "profiles.teams": {
                    "type": "teams"
                }
            },
            "linked": {
                "job_titles": [
                    {
                        "id": "3be1c271-2be0-459d-b587-d2911354dbca",
                        "parent_id": "853e4a3c-a9c3-4f38-8f79-3aa9b80e1266",
                        "title": "Chief Executife Officer",
                        "links": {
                            "job_tier": "853e4a3c-a9c3-4f38-8f79-3aa9b80e1266"
                        },
                        "active": true
                    },
                    ...
                ],
                "files": [],
                "groups": [
                    {
                        "id": "c2bad067-6f48-4a4b-8b25-06c16bebc145",
                        "title": "Your Company",
                        "type": "Subsidiary",
                        "is_team": true,
                        "address": null,
                        "count": 0,
                        "links": {
                            "group_type": "1ab11dab-c4eb-45ab-1be2-dbed5a1f5f1e"
                        }
                    },
                    ...
                ],
                "teams": []
            }
        }

        Raises
        ------
        EntityNotFound - when response status code is 404
        AccessDenied - when response status code is 403
        RequestError - when response status code is other 400 error
        """

        filters = {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "personal_email": personal_email,
            "job_title": job_title,
            "reports_to": reports_to,
            "user_status": user_status,
            "limit": limit,
        }
        if not any(filters.values()):
            return {
                "message": f"Error. You need to specify at least one of the following filters: "
                f"{', '.join([key for key in filters.keys()])} or use `get_all` method."
            }
        logging.info("Starting getting all profiles from Namely with applied filters")
        all_profiles = []
        path = "profiles.json?page={}&per_page={}&{}"
        filter_query = "&".join(
            [f"filter[{key}]={value}" for key, value in filters.items() if value]
        )
        response = self._get_json(path.format(1, 2, filter_query))
        total_count = response["meta"]["total_count"]
        logging.info(f"There is {total_count} profiles")

        pages = range(1, (total_count // limit) + 2)
        futures = []
        links = response["links"]
        linked = {
            "job_titles": [],
            "files": [],
            "groups": [],
            "teams": [],
        }
        job_titles_added, groups_added, files_added, teams = {}, {}, {}, {}
        with ThreadPoolExecutor() as executor:
            for page in pages:
                future = executor.submit(self._get_json, path.format(page, limit, filter_query))
                futures.append(future)
        for future in futures:
            try:
                result = future.result()
            except Exception as err:
                logging.exception(
                    "Exception in ThreadPoolExecutor",
                    extra={"extra": {"error": str(err)}},
                )
            else:
                if result and result.get("profiles"):
                    all_profiles.extend(result["profiles"])
                    linked["job_titles"].extend(
                        [
                            job_title
                            for job_title in result["linked"]["job_titles"]
                            if not job_titles_added.get(job_title["id"])
                        ]
                    )
                    job_titles_added.update(
                        {job_title["id"]: None for job_title in result["linked"]["job_titles"]}
                    )
                    linked["groups"].extend(
                        [
                            group
                            for group in result["linked"]["groups"]
                            if not groups_added.get(group["id"])
                        ]
                    )
                    groups_added.update({group["id"]: None for group in result["linked"]["groups"]})
                    linked["files"].extend(
                        [
                            file
                            for file in result["linked"]["files"]
                            if not files_added.get(file["id"])
                        ]
                    )
                    files_added.update({file["id"]: None for file in result["linked"]["files"]})
                    linked["teams"].extend(
                        [team for team in result["linked"]["teams"] if not teams.get(team["id"])]
                    )
                    teams.update({team["id"]: None for team in result["linked"]["teams"]})
        logging.info(f"Returning {len(all_profiles)} profiles")
        return {
            "profiles": all_profiles,
            "meta": {"total_count": total_count},
            "links": links,
            "linked": linked,
        }

    @retry(stop_max_attempt_number=STOP_MAX_ATTEMPT_NUMBER, wait_fixed=WAIT_FIXED)
    def update(self, _id: str, profile: Dict) -> Dict:
        """
        Update Namely profile by Namely profile id

        Parameters
        ----------
        _id : str, required
            Namely profile id.
            Example: `051f9e32-4365-4ad3-a60f-572a76a41ce1`
        profile: dict, required
            Dictionary with all items to update, for example `{"user_status": "inactive", ... }

        See Also
        --------
        Profile.create : method to create a new Namely.

        Examples
        --------
        Using `update` method.

        >>> from namely import Client
        >>> client = Client("https://your-company.namely/api/v1/", "your-namely-api-token")
        >>> profile_to_update = {"user_status": "inactive"}
        >>> updated_profile = client.profiles.update(
        "namely-profile-id-to-update",
        profile_to_update
        )
        >>> updated_profile
        {
            "profiles": [
                {
                    "id": "namely-profile-id",
                    "company_uuid": "109fbc88-8cac-45fb-bddb-ebd0d5a8c0b4",
                    "email": "john.doe@your-company.com",
                    "first_name": "John",
                    "last_name": "Doe",
                    "user_status": "inactive",
                    "preferred_name": "Jo",
                    ""full_name": "Jo Doe",
                    "job_title": {
                        "id": "3be1c271-2be0-459d-b587-d2911354dbca",
                        "title": "Chief Executife Officer"
                    },
                    "links": {
                        "job_title": {
                            "id": "3be1c271-2be0-459d-b587-d2911354dbca",
                            "title": "Chief Executife Officer"
                        },
                        "groups": [
                            {
                                "id": "c2bad067-6f48-4a4b-8b25-06c16bebc145",
                                "name": "Your Company"
                            },
                        ],
                        "teams": []
                    },
                    ...
                },
                ...
            ],
            "meta": {
                "count": 1,
                "status": 200,
                "total_count": 1
            },
            "links": {
                "profiles.job_title": {
                    "type": "job_titles"
                },
                "profiles.image": {
                    "type": "files"
                },
                "profiles.groups": {
                    "type": "groups"
                },
                "profiles.teams": {
                    "type": "teams"
                }
            },
            "linked": {
                "job_titles": [
                    {
                        "id": "3be1c271-2be0-459d-b587-d2911354dbca",
                        "parent_id": "853e4a3c-a9c3-4f38-8f79-3aa9b80e1266",
                        "title": "Chief Executife Officer",
                        "links": {
                            "job_tier": "853e4a3c-a9c3-4f38-8f79-3aa9b80e1266"
                        },
                        "active": true
                    },
                    ...
                ],
                "files": [],
                "groups": [
                    {
                        "id": "c2bad067-6f48-4a4b-8b25-06c16bebc145",
                        "title": "Your Company",
                        "type": "Subsidiary",
                        "is_team": true,
                        "address": null,
                        "count": 0,
                        "links": {
                            "group_type": "1ab11dab-c4eb-45ab-1be2-dbed5a1f5f1e"
                        }
                    },
                    ...
                ],
                "teams": []
            }
        }

        Raises
        ------
        requests.HTTPError - when response status code is not OK
        """

        logging.info("Starting updating Namely profile by id")
        payload = {"profiles": [profile]}
        response = self.session.put(f"profiles/{_id}.json", payload)
        response.raise_for_status()

        return response.json()

    @retry(stop_max_attempt_number=STOP_MAX_ATTEMPT_NUMBER, wait_fixed=WAIT_FIXED)
    def create(self, profile: Dict) -> Dict:
        """
        Create Namely profile with the necessary fields

        Parameters
        ----------
        profile: dict, required
            Dictionary with all the necessary items to create, for example:
            {
                "first_name": "John",                    # REQUIRED
                "last_name": "Smith",                    # REQUIRED
                "user_status": "pending",                # REQUIRED
                "start_date": "2019-01-01",              # REQUIRED
                "email": "work@email.com",               # REQUIRED
                "personal_email": "personal@email.com",  # REQUIRED if `user_staus` is `pending`
                "job_title": {
                    "id": "a4d5783d-a447-4269-8724-b710d0267aa4"
                },
                "home": {
                    "address1": "195 Broadway",
                    "address2": "",
                    "city": "New York",
                    "state_id": "NY",
                    "country_id": "US",
                    "zip": "10007"
                },
                "salary": {
                    "currency_type": "USD",
                    "date": "2019-01-10",
                    "yearly_amount": 100000
            }

        See Also
        --------
        Profile.update : method to update a new Namely.

        Examples
        --------
        Using `create` method.

        >>> from namely import Client
        >>> client = Client("https://your-company.namely/api/v1/", "your-namely-api-token")
        >>> new_profile = {
            "first_name": "John",
            "last_name": "Smith",
            "user_status": "active",
            "start_date": "2019-01-01",
            "email": "work@email.com"
            }
        >>> created_profile = client.profiles.create(new_profile)
        >>> created_profile
        {
            "profiles": [
                {
                    "id": "namely-profile-id",
                    "first_name": "John",
                    "last_name": "Smith",
                    "user_status": "active",
                    ""start_date": "Jo Doe",
                    "email": "work@email.com"
                    ...
                },
                ...
            ],
            "meta": {
                "count": 1,
                "status": 200,
                "total_count": 1
            },
            "links": {
                "profiles.job_title": {
                    "type": "job_titles"
                },
                "profiles.image": {
                    "type": "files"
                },
                "profiles.groups": {
                    "type": "groups"
                },
                "profiles.teams": {
                    "type": "teams"
                }
            },
            "linked": {
                "job_titles": [],
                "files": [],
                "groups": [],
                "teams": []
            }
        }

        Raises
        ------
        requests.HTTPError - when response status code is not OK
        """

        logging.info("Starting creating a new Namely profile")
        payload = {"profiles": [profile]}
        response = self.session.post("profiles.json", payload)
        response.raise_for_status()

        return response.json()
