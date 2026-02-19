import pytest
import requests
from faker import Faker

from Cinescope_exam.api.api_manager import ApiManager
from Cinescope_exam.constants import BASE_URL, ADMIN_USERNAME, ADMIN_PASSWORD, LOGIN_ENDPOINT
from Cinescope_exam.custom_requester.custom_requester import CustomRequester
from Cinescope_exam.resources.user_creds import SuperAdminCreds
from Cinescope_exam.entities.user import User

print(SuperAdminCreds.USERNAME, SuperAdminCreds.PASSWORD)