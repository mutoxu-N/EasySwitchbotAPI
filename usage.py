from pprint import pprint
from easy_switchbot.api import SwitchbotAPI
from easy_switchbot.devices import *
import time

sAPI = SwitchbotAPI(
    token="",
    secret=""
)

all_devices = sAPI.devices

print("All devices")
pprint(all_devices)

devices = sAPI.get_devices(["X00X0000000X"])
smart_plug: PlugMiniJP = devices["X00X0000000X"]

print("Status:", smart_plug)
pprint(sAPI.status(smart_plug))


print("Turn on")
sAPI.run(smart_plug.command_turn_on())

time.sleep(3)

print("Turn off")
sAPI.run(smart_plug.command_turn_off())
