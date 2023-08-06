"""Module for `profiles` resource"""
import logging
from typing import Dict, Union, List

from retrying import retry

from .._config import STOP_MAX_ATTEMPT_NUMBER, WAIT_FIXED
from .helpers import BaseResource


class Profile(BaseResource):
    """
    A class used to operate `profiles` resource

    Methods:
     - :py:meth:`~Profile.get_all` Returns all Namely profiles
     - :py:meth:`~Profile.get` Returns a Namely profile by profile id
     - :py:meth:`~Profile.get_me` Returns current user's Namely profile
     - :py:meth:`~Profile.filter` Returns all Namely profiles with applied filters
     - :py:meth:`~Profile.update` Updates Namely profile by id
     - :py:meth:`~Profile.create` Creates a new Namely profile
    """

    def _get_all_synchronously(
        self, pages: List[int], path: str, links: List, total_count: int, *args
    ) -> Dict[str, Union[str, int, float, bool, List[Dict[str, Union[str, int, float, bool]]]]]:
        all_profiles = []
        linked = {
            "job_titles": [],
            "files": [],
            "groups": [],
            "teams": [],
        }
        job_titles_added, groups_added, files_added, teams = {}, {}, {}, {}
        for page in pages:
            try:
                result = self._get_json(path.format(page, *args))
            except Exception as err:
                logging.exception(
                    "Exception in _get_json",
                    extra={"extra": {"error": str(err)}},
                )
            else:
                if result and result.get("profiles"):
                    self._process_result(
                        all_profiles,
                        files_added,
                        groups_added,
                        job_titles_added,
                        linked,
                        result,
                        teams,
                    )
        logging.info(f"Returning {len(all_profiles)} profiles")
        return {
            "profiles": all_profiles,
            "meta": {"total_count": total_count},
            "links": links,
            "linked": linked,
        }

    @staticmethod
    def _process_result(
        all_profiles, files_added, groups_added, job_titles_added, linked, result, teams
    ):
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
            [group for group in result["linked"]["groups"] if not groups_added.get(group["id"])]
        )
        groups_added.update({group["id"]: None for group in result["linked"]["groups"]})
        linked["files"].extend(
            [file for file in result["linked"]["files"] if not files_added.get(file["id"])]
        )
        files_added.update({file["id"]: None for file in result["linked"]["files"]})
        linked["teams"].extend(
            [team for team in result["linked"]["teams"] if not teams.get(team["id"])]
        )
        teams.update({team["id"]: None for team in result["linked"]["teams"]})

    def _get_all_in_multi_threads(
        self, pages: List[int], path: str, links: List, total_count: int, *args
    ) -> Dict[str, Union[str, int, float, bool, List[Dict[str, Union[str, int, float, bool]]]]]:
        from concurrent.futures import ThreadPoolExecutor

        all_profiles = []
        futures = []

        linked = {
            "job_titles": [],
            "files": [],
            "groups": [],
            "teams": [],
        }
        job_titles_added, groups_added, files_added, teams = {}, {}, {}, {}
        with ThreadPoolExecutor() as executor:
            for page in pages:
                formatted_path = path.format(page, *args)
                future = executor.submit(self._get_json, formatted_path)
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
                    self._process_result(
                        all_profiles,
                        files_added,
                        groups_added,
                        job_titles_added,
                        linked,
                        result,
                        teams,
                    )
        logging.info(f"Returning {len(all_profiles)} profiles")
        return {
            "profiles": all_profiles,
            "meta": {"total_count": total_count},
            "links": links,
            "linked": linked,
        }

    @retry(stop_max_attempt_number=STOP_MAX_ATTEMPT_NUMBER, wait_fixed=WAIT_FIXED)
    def get_all(
        self, limit: int = 50, multi_threading: bool = True
    ) -> Dict[str, Union[str, int, float, bool]]:
        """
        Returns all Namely profiles.

        .. note:: This method returns all profiles with all fields based on user (who generated token) permissions.

        :param limit: A number of profiles to get from Namely per request, defaults to `50`
        :type limit: int, optional
        :param multi_threading: An option to send requests to Namely API synchronously or in multiple threads,
           defaults to `True`
        :type multi_threading: bool, optional
        :returns: a dict with Namely response.
        :exception EntityNotFound: when response status code is 404
        :exception AccessDenied: when response status code is 403
        :exception RequestError: when response status code is other 400 error

        See Also methods:
         - :py:meth:`~Profile.get` method to get profile by Namely id
         - :py:meth:`~Profile.get_me` method to get current user's profile
         - :py:meth:`~Profile.filter` method to get filtered profiles

        Example of using :py:meth:`~Profile.get_all` method.

        >>> from namely import Client
        >>> client = Client("https://your-company.namely/api/v1/", "your-namely-api-token")
        >>> profiles = client.profiles.get_all(limit=10)
        >>> profiles
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
        """

        logging.info("Starting getting all profiles from Namely")
        path = "profiles.json?page={}&per_page={}"
        response = self._get_json(path.format(1, 2))
        total_count = response["meta"]["total_count"]
        logging.info(f"There is {total_count} profiles")

        pages = list(range(1, (total_count // limit) + 2))
        links = response["links"]
        if multi_threading:
            return self._get_all_in_multi_threads(pages, path, links, total_count, limit)

        return self._get_all_synchronously(pages, path, links, total_count, limit)

    @retry(stop_max_attempt_number=STOP_MAX_ATTEMPT_NUMBER, wait_fixed=WAIT_FIXED)
    def get(self, _id: str) -> Dict[str, Union[str, int, float, bool]]:
        """
        Returns a Namely profile by Namely profile id

        .. note:: This method returns a profile with all fields based on user (who generated token) permissions.

        :param _id: A Namely profile id
        :type _id: str, required
        :returns: a dict with Namely response.
        :exception EntityNotFound: when response status code is 404
        :exception AccessDenied: when response status code is 403
        :exception RequestError: when response status code is other 400 error

        See Also methods:
         - :py:meth:`~Profile.get_all` method to get all profiles
         - :py:meth:`~Profile.get_me` method to get current user's profile
         - :py:meth:`~Profile.filter` method to get filtered profiles

        Example of using :py:meth:`~Profile.get` method.

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
        """

        logging.info("Starting getting Namely profile by id")
        return self._get_json(f"profiles/{_id}.json")

    @retry(stop_max_attempt_number=STOP_MAX_ATTEMPT_NUMBER, wait_fixed=WAIT_FIXED)
    def get_me(self) -> Dict[str, Union[str, int, float, bool]]:
        """
        Returns current user's Namely profile

        .. note:: This method returns current user profile with all fields based on user
           (who generated token) permissions.

        :returns: a dict with Namely response.
        :exception EntityNotFound: when response status code is 404
        :exception AccessDenied: when response status code is 403
        :exception RequestError: when response status code is other 400 error

        See Also methods:
         - :py:meth:`~Profile.get_all` method to get all profiles
         - :py:meth:`~Profile.get` method to get profile by Namely id
         - :py:meth:`~Profile.filter` method to get filtered profiles

        Example of using :py:meth:`~Profile.get_me` method.

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
        multi_threading: bool = True,
    ) -> Dict[str, Union[str, int, float, bool]]:
        """
        Returns all Namely profiles with applied filters.

        .. note:: This method returns all profiles based on applied filterswith all fields based on user
           (who generated token) permissions.

        .. note:: Reuires using at least one filter.

        :param first_name: Employees `first_name`, for example `John`, defaults to `None`
        :type first_name: str, optional
        :param last_name: Employees `last_name`, for example `Doe`, defaults to `None`
        :type last_name: str, optional
        :param email: Employees company email, for example `john.doe@your-company.com`, defaults to `None`
        :type email: str, optional
        :param personal_email: Employees `personal_email`, for example `john.doe@email.com`, defaults to `None`
        :type personal_email: str, optional
        :param job_title: Employees `job_title`, for example `HR Admin`, defaults to `None`
        :type job_title: str, optional
        :param reports_to: Employees `reports_to`, (manager) Namely id, for example
           `8be1c671-2be4-452d-b587-d2711354dbcc`, defaults to `None`
        :type reports_to: str, optional
        :param user_status: Employees `user_status`, can be one of the options: `active`, `inactive`, `pending`,
           defaults to `None`
        :type user_status: str, optional
        :param limit: A number of profiles to get from Namely per request, defaults to `50`
        :type limit: int, optional
        :param multi_threading: An option to send requests to Namely API synchronously or in multiple threads,
           defaults to `True`
        :type multi_threading: bool, optional
        :returns: a dict with Namely response.
        :exception EntityNotFound: when response status code is 404
        :exception AccessDenied: when response status code is 403
        :exception RequestError: when response status code is other 400 error

        See Also methods:
         - :py:meth:`~Profile.get_all` method to get all profiles
         - :py:meth:`~Profile.get` method to get profile by Namely id
         - :py:meth:`~Profile.get_me` method to get current user's profile

        Example of using :py:meth:`~Profile.filter` method.

        >>> from namely import Client
        >>> client = Client("https://your-company.namely/api/v1/", "your-namely-api-token")
        >>> filtered_profiles = client.profiles.filter(email="john.doe@your-company.com", limit=1)
        >>> filtered_profiles
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
        path = "profiles.json?page={}&per_page={}&{}"
        filter_query = "&".join(
            [f"filter[{key}]={value}" for key, value in filters.items() if value]
        )
        response = self._get_json(path.format(1, 2, filter_query))
        total_count = response["meta"]["total_count"]
        logging.info(f"There is {total_count} profiles")

        pages = list(range(1, (total_count // limit) + 2))
        links = response["links"]

        if multi_threading:
            return self._get_all_in_multi_threads(
                pages, path, links, total_count, limit, filter_query
            )

        return self._get_all_synchronously(pages, path, links, total_count, limit, filter_query)

    @retry(stop_max_attempt_number=STOP_MAX_ATTEMPT_NUMBER, wait_fixed=WAIT_FIXED)
    def update(
        self, _id: str, profile: Dict[str, Union[str, int, float, bool]]
    ) -> Dict[str, Union[str, int, float, bool]]:
        """
        Update Namely profile by Namely profile id

        :param _id: A Namely profile id
        :type _id: str, required
        :param profile: A dictionary with profile fields to update
        :type profile: dict, required
        :returns: a dict with Namely response.
        :exception requests.HTTPError: when response status code is not OK

        See Also methods:
         - :py:meth:`~Profile.create` method to create a new Namely

        Example of using :py:meth:`~Profile.update` method.

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
        """

        logging.info("Starting updating Namely profile by id")
        payload = {"profiles": [profile]}
        response = self.session.put(f"profiles/{_id}.json", payload)
        response.raise_for_status()

        return response.json()

    @retry(stop_max_attempt_number=STOP_MAX_ATTEMPT_NUMBER, wait_fixed=WAIT_FIXED)
    def create(
        self, profile: Dict[str, Union[str, int, float, bool]]
    ) -> Dict[str, Union[str, int, float, bool]]:
        """
        Create Namely profile with the necessary fields

        :param profile: Dictionary with all the necessary items to create, see example:
        :type profile: dict, required
        :returns: a dict with Namely response.
        :exception requests.HTTPError: when response status code is not OK

        See Also methods:
         - :py:meth:`~Profile.update` method to update a Namely

        Example of using :py:meth:`~Profile.create` method.


        >>> from namely import Client
        >>> client = Client("https://your-company.namely/api/v1/", "your-namely-api-token")
        >>> new_profile = {
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
        """

        logging.info("Starting creating a new Namely profile")
        payload = {"profiles": [profile]}
        response = self.session.post("profiles.json", payload)
        response.raise_for_status()

        return response.json()
