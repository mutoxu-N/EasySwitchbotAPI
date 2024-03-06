from pprint import pprint
from switchbot_api.api import SwitchbotAPI

sAPI = SwitchbotAPI(
    token="",
    secret="")

json = sAPI.get("devices")
pprint(json)
