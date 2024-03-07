import json


class SwitchbotDevice:
    """parent class of switchbot devices
    """

    def __init__(
            self,
            device_id: str,
            device_name: str,
            enable_cloud_service: bool,
            hub_device_id: str) -> None:
        """the constructor for SwitchbotDevice

        Args:
            device_id (str): the id of the device
            device_name (str): the name of the device
            enable_cloud_service (bool): whether device enable the cloud service or not
            hub_device_id (str): if the device has any parents, show their ids.
        """

        self._device_id = device_id
        self._device_name = device_name
        self._enable_cloud_service = enable_cloud_service
        self._hub_device_id = hub_device_id

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(id: {self._device_id}, name: {self._device_name})"

    @property
    def device_id(self) -> str:
        return self._device_id

    @property
    def device_name(self) -> str:
        return self._device_name

    @property
    def enable_cloud_service(self) -> bool:
        return self._enable_cloud_service

    @property
    def hub_device_id(self) -> str:
        return self._hub_device_id


class Bot(SwitchbotDevice):
    def __init__(
            self,
            device_id: str,
            device_name: str,
            enable_cloud_service: bool,
            hub_device_id: str) -> None:
        super().__init__(device_id, device_name, enable_cloud_service, hub_device_id)

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

    def command_press(self) -> str:
        return json.dumps({
            "command": "press",
            "commandType": "command",
            "parameter": "default",
        })


class Curtain(SwitchbotDevice):
    def __init__(
            self,
            device_id: str,
            device_name: str,
            enable_cloud_service: bool,
            hub_device_id: str,
            curtain_device_ids: str,
            calibrate: bool,
            group: bool,
            master: bool,
            openDirection: str) -> None:
        super().__init__(device_id, device_name, enable_cloud_service, hub_device_id)
        self._curtain_device_ids = curtain_device_ids
        self._calibrate = calibrate
        self._group = group
        self._master = master
        self._openDirection = openDirection

    @property
    def curtain_device_ids(self) -> str:
        return self._curtain_device_ids

    @property
    def calibrate(self) -> bool:
        return self._calibrate

    @property
    def group(self) -> bool:
        return self._group

    @property
    def master(self) -> bool:
        return self._master

    @property
    def openDirection(self) -> str:
        return self._openDirection

    def command_set_position(index: int, mode: str, position: int):
        """set curtain position

        * mode
        0: Performance Mode
        1: Silent Mode
        ff: default mode

        * position
        0 means open
        100 means closed
        """
        return json.dumps({
            "command": "setPosition",
            "commandType": "command",
            "parameter": f"{index},{mode},{position}",
        })

    def command_open(self) -> str:
        return json.dumps({
            "command": "turnOn",
            "commandType": "command",
            "parameter": "default",
        })

    def command_close(self) -> str:
        return json.dumps({
            "command": "turnOff",
            "commandType": "command",
            "parameter": "default",
        })

    def command_pause(self) -> str:
        return json.dumps({
            "command": "pause",
            "commandType": "command",
            "parameter": "default",
        })


class Curtain3(Curtain):
    def __init__(self, device_id: str, device_name: str, enable_cloud_service: bool, hub_device_id: str, curtain_device_ids: str, calibrate: bool, group: bool, master: bool, openDirection: str) -> None:
        super().__init__(device_id, device_name, enable_cloud_service, hub_device_id,
                         curtain_device_ids, calibrate, group, master, openDirection)


class PlugMiniUS(SwitchbotDevice):
    def __init__(
            self,
            device_id: str,
            device_name: str,
            enable_cloud_service: bool,
            hub_device_id: str) -> None:
        super().__init__(device_id, device_name, enable_cloud_service, hub_device_id)

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

    def command_toggle(self) -> str:
        return json.dumps({
            "command": "toggle",
            "commandType": "command",
            "parameter": "default",
        })


class PlugMiniJP(PlugMiniUS):
    def __init__(self, device_id: str, device_name: str, enable_cloud_service: bool, hub_device_id: str) -> None:
        super().__init__(device_id, device_name, enable_cloud_service, hub_device_id)
