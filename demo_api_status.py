#Test to API status after authentication
from browserstack import *

USER_NAME = ""
API_KEY = ""
BS_API = BSAPI(USER_NAME,API_KEY)
print BS_API.getStatus()