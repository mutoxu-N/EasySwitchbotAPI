from switchbot_api.devices import Device
import json


class InfraredDevice(Device):
    """parent class of infrared devices
    """

    def command_turn_on(self) -> str:
        return json.dumps({
            "command": "turnOn",
            "commandType": "command",
            "parameter": "default",
        })

    def command_turn_off(self) -> str:
        return json.dumps({
            "command": "turnOff",
            "commandType": "command",
            "parameter": "default",
        })


class OtherInfrared(InfraredDevice):
    def __init__(
            self,
            device_id: str,
            device_name: str,
            remote_type: str,
            hub_device_id: str) -> None:
        """the constructor for InfraredDevice

        Args:
            device_id (str): the id of the device
            device_name (str): the name of the device
            remote_type (str): the type of the device
            hub_device_id (str): if the device has any parents, show their ids.
        """
        super().__init__(device_id, device_name, hub_device_id)
        self._remote_type = remote_type

    @property
    def remote_type(self) -> str: return self._remote_type

    def command_run(self, command: str) -> str:
        """
        * command
        user-defined button name
        """
        return json.dumps({
            "command": command,
            "commandType": "customize",
            "parameter": "default",
        })


class AirConditionerInfrared(InfraredDevice):
    def command_set(self, temp: int, mode: int, fan_speed: int, power_state: str) -> str:
        """
        * power_state on/off
        """
        return json.dumps({
            "command": "setAll",
            "commandType": "command",
            "parameter": f"{temp},{mode},{fan_speed},{power_state}",
        })
