from pprint import pprint
from switchbot_api.api import SwitchbotAPI
from switchbot_api.devices import *

sAPI = SwitchbotAPI(
    token="",
    secret="")

devices = sAPI.devices
smart_plug: PlugMiniJP = devices[0]

print("target:", smart_plug)
print("turn on")
sAPI.run(smart_plug.device_id, smart_plug.command_turn_on())

time.sleep(10)

print("turn off")
sAPI.run(smart_plug.device_id, smart_plug.command_turn_off())
