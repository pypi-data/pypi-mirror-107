import json
import logging

import requests

from enum import Enum

logger = logging.getLogger(__name__)

ACCESS_TOKEN_EXPIRED = 124


class PaidAccountException(Exception):
    def __init__(self):
        return super().__init__("Paid account required to run this request.")


class ZoomLoginTypes(Enum):
    FACEBOOK = 0
    GOOGLE = 1
    API = 99
    ZOOM = 100
    SSO = 101


class ZoomClient:
    endpoint = "https://api.zoom.us/v2"
    """
    A thin client around Zoom API http requests
    """
    def __init__(self, access_token):
        self.access_token = access_token

    def __zoom_headers(self):
        return {
            'authorization': f"Bearer {self.access_token}",
            'content-type': "application/json"
        }

    def get_request(self, path, params=None):
        try:

            headers = self.__zoom_headers()
            full_path = f"{self.endpoint}{path}"
            resp = requests.get(full_path, headers=headers, params=params)
            parsed_resp = json.loads(resp.text)

            if parsed_resp.get("code") == 200:
                raise PaidAccountException()

            return parsed_resp

        except Exception as e:
            logger.exception(e)
            return None

    def paginated_request(self,
                          base_path,
                          key=None,
                          page_number=None,
                          additional_params={}):

        if not key:
            raise Exception(
                "Missing a key to use for retrieving paginated data. Check the Zoom API docs to find the key associated with the list of results"
            )

        items = []
        page_size = 30
        params = {"page_size": page_size, **additional_params}

        if page_number:
            params["page_number"] = page_number

        paginated_results = self.get_request(base_path, params=params)

        if paginated_results:
            next_page_token = paginated_results.get("next_page_token")
            items = paginated_results.get(key, [])

            while next_page_token is not None and next_page_token != '':
                if page_number:
                    page_number += 1

                updated_params = {
                    "page_number": page_number,
                    "next_page_token": next_page_token,
                    **params
                }

                paginated_response = self.get_request(base_path,
                                                      params=updated_params)

                next_page_token = paginated_response.get("next_page_token")

                items.extend(paginated_response.get(key))

        return items

    def get_user(self, user_id):
        """
        Fetch user info
        """
        user_response = self.get_request(f"/users/{user_id}")

        return user_response

    def get_user_permissions(self, user_id):
        """
        Fetch permissions a zoom user has.
        
        returns: a list(str) of permissions.
        """

        user_permission_response = self.get_request(
            f"/users/{user_id}/permissions")

        return user_permission_response

    def get_user_login_type(self, user_obj):
        """
        Given an object returned by get_user(id), 
        return human-readable login method associated with the user
        """
        types = []
        login_types = user_obj.get("login_types")

        for login_type in login_types:

            if login_type == ZoomLoginTypes.FACEBOOK.value:
                types.append(ZoomLoginTypes.FACEBOOK.name)

            elif login_type == ZoomLoginTypes.GOOGLE.value:
                types.append(ZoomLoginTypes.GOOGLE.name)

            elif login_type == ZoomLoginTypes.API.value:
                types.append(ZoomLoginTypes.API.name)

            elif login_type == ZoomLoginTypes.ZOOM.value:
                types.append(ZoomLoginTypes.ZOOM.name)

            elif login_type == ZoomLoginTypes.SSO.value:
                types.append(ZoomLoginTypes.SSO.name)

        return types

    def get_users(self):
        """
        Fetch user info return a list of users.
        """

        return self.paginated_request("/users", key="users")

    def get_meetings(self, user_id):
        return self.paginated_request(f"/users/{user_id}/meetings",
                                      key="meetings")

    def get_meeting(self, meeting_id):
        return self.get_request(f"/meetings/{meeting_id}")

    def get_cloud_recordings(self, user_id):
        """
        Get the list of cloud recordings associated with a user
        """

        cloud_recordings = self.paginated_request(
            f"/users/{user_id}/recordings", key="meetings")

        return cloud_recordings

    def get_meeting_recordings(self, meeting_id):
        """
         Get all the recordings from a meeting or webinar instance
        """
        return self.get_request(f"/meetings/{meeting_id}/recordings")

    def get_im_groups(self):
        return self.get_request("/im/groups")

    def get_operation_logs(
        self,
        category_type="all",
        date_from=None,
        date_to=None,
    ):
        params = {"category_type": category_type}

        if date_from:
            params["from"] = date_from
        if date_to:
            params["to"] = date_to

        operation_logs = self.paginated_request("/report/operationlogs",
                                                key="operation_logs",
                                                additional_params=params)

        return operation_logs

    def get_roles(self):
        roles = []
        try:
            roles_resp = self.get_request("/roles")
            roles = roles_resp.get("roles") if roles_resp.get("roles") else []

        except Exception as e:
            print(e)

        return roles
