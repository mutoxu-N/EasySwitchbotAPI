from pprint import pprint
from easy_switchbot.api import SwitchbotAPI
from easy_switchbot.devices import *
from easy_switchbot.statuses import *
import time

sAPI = SwitchbotAPI(
    token="",
    secret=""
)

print("All devices")
all_devices = sAPI.devices
pprint(all_devices)

devices = sAPI.get_devices(["X00X0000000X"])
plug_mini: PlugMiniJP = devices["X00X0000000X"]
plug_status: PlugMiniJPStatus = sAPI.status(plug_mini)

print("\nStatus:", plug_mini)
print(f"  └ {plug_status}")
print(f"      ├ deviceId={plug_status.device_id}")
print(f"      ├ hubDeviceId={plug_status.hub_device_id}")
print(f"      ├ voltage={plug_status.voltage}")
print(f"      ├ version={plug_status.version}")
print(f"      ├ weight={plug_status.weight}")
print(f"      ├ electricityOfDay={plug_status.electricity_of_day}")
print(f"      └ electricCurrent={plug_status.electric_current}")


print("\nTurn on")
sAPI.run(plug_mini.command_turn_on())

time.sleep(3)

print("Turn off")
sAPI.run(plug_mini.command_turn_off())
