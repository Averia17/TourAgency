from typing import Dict, Any

import requests
from django.conf import settings
from rest_framework.exceptions import ValidationError

GOOGLE_ID_TOKEN_INFO_URL = "https://www.googleapis.com/oauth2/v3/tokeninfo"


#
# def google_get_access_token(code: str, redirect_uri: str) -> str:
#     data = {
#         "code": code,
#         "client_id": GOOGLE_OAUTH2_CLIENT_ID,
#         "client_secret": GOOGLE_OAUTH2_CLIENT_SECRET,
#         "redirect_uri": redirect_uri,
#         "grant_type": "authorization_code",
#     }
#     response = requests.post(GOOGLE_ACCESS_TOKEN_OBTAIN_URL, data=data)
#     if not response.ok:
#         raise ValidationError("Failed to obtain access token from Google.")
#     access_token = response.json()["access_token"]
#     return access_token
#
#
# def google_get_user_info(access_token: str) -> Dict[str, Any]:
#     response = requests.get(GOOGLE_USER_INFO_URL, params={"access_token": access_token})
#     if not response.ok:
#         raise ValidationError("Failed to obtain user info from Google.")
#     return response.json()
#


def google_validate_id_token(id_token: str) -> bool:
    response = requests.get(GOOGLE_ID_TOKEN_INFO_URL, params={"id_token": id_token})
    if not response.ok:
        raise ValidationError("id_token is invalid.")
    audience = response.json()["aud"]
    if audience != settings.GOOGLE_OAUTH2_CLIENT_ID:
        raise ValidationError("Invalid audience.")
    return True
