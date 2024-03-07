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

    def __str__(
        self) -> str: return f"{self.__class__.__name__}(id: {self._device_id}, name: {self._device_name})"

    @property
    def device_id(self) -> str: return self._device_id

    @property
    def device_name(self) -> str: return self._device_name

    @property
    def enable_cloud_service(self) -> bool: return self._enable_cloud_service

    @property
    def hub_device_id(self) -> str: return self._hub_device_id


class Bot(SwitchbotDevice):
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
            curtain_device_ids: list,
            calibrate: bool,
            group: bool,
            master: bool,
            openDirection: str) -> None:
        super().__init__(device_id, device_name, enable_cloud_service, hub_device_id)
        self._curtain_device_ids = tuple(curtain_device_ids)
        self._calibrate = calibrate
        self._group = group
        self._master = master
        self._openDirection = openDirection

    @property
    def curtain_device_ids(self) -> tuple: return self._curtain_device_ids

    @property
    def calibrate(self) -> bool: return self._calibrate

    @property
    def group(self) -> bool: return self._group

    @property
    def master(self) -> bool: return self._master

    @property
    def openDirection(self) -> str: return self._openDirection

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
    pass


class Hub(SwitchbotDevice):
    pass


class HubPlus(Hub):
    pass


class HubMini(Hub):
    pass


class Hub2(Hub):
    pass


class Meter(SwitchbotDevice):
    pass


class MeterPlus(Meter):
    pass


class OutdoorMeter(Meter):
    pass


class Lock(SwitchbotDevice):
    def __init__(
            self,
            device_id: str,
            device_name: str,
            enable_cloud_service: bool,
            hub_device_id: str,
            group: bool,
            master: bool,
            group_name: str,
            lock_device_ids: list) -> None:
        super().__init__(device_id, device_name, enable_cloud_service, hub_device_id)
        self._group = group
        self._master = master
        self._group_name = group_name
        self._lock_device_ids = tuple(lock_device_ids)

    @property
    def group(self) -> bool: return self._group

    @property
    def master(self) -> bool: return self._master

    @property
    def group_name(self) -> str: return self._group_name

    @property
    def lock_device_ids(self) -> tuple: return self._lock_device_ids

    def command_lock(self) -> str:
        return json.dumps({
            "command": "lock",
            "commandType": "command",
            "parameter": "default",
        })

    def command_unlock(self) -> str:
        return json.dumps({
            "command": "unlock",
            "commandType": "command",
            "parameter": "default",
        })


class Keypad(SwitchbotDevice):
    class Key:
        def __init__(
                self,
                id: int,
                name: str,
                type: str,
                password: str,
                iv: str,
                status: str,
                createTime: int) -> None:
            self._id = id
            self._name = name
            self._type = type
            self._password = password
            self._iv = iv
            self._status = status
            self._createTime = createTime

        @property
        def id(self) -> int: return self._id

        @property
        def name(self) -> str: return self._name

        @property
        def type(self) -> str: return self._type

        @property
        def password(self) -> str: return self._password

        @property
        def iv(self) -> str: return self._iv

        @property
        def status(self) -> str: return self._status

        @property
        def createTime(self) -> int: return self._createTime

    def __init__(
            self,
            device_id: str,
            device_name: str,
            enable_cloud_service: bool,
            hub_device_id: str,
            lock_device_id: str,
            key_list: list) -> None:
        super().__init__(device_id, device_name, enable_cloud_service, hub_device_id)
        self._lock_device_id = tuple(lock_device_id)

        l = []
        for key in key_list:
            l.append(self.Key(
                int(key["id"]),
                key["name"],
                key["type"],
                key["password"],
                key["iv"],
                key["status"],
                int(key["createTime"]),
            ))
        self._key_list = tuple(l)

    @property
    def lock_device_id(self) -> str: return self._lock_device_id

    @property
    def key_list(self) -> tuple: return self._key_list


class KeypadTouch(Keypad):
    pass


class Remote(SwitchbotDevice):
    pass


class MotionSensor(SwitchbotDevice):
    pass


class ContactSensor(SwitchbotDevice):
    pass


class CeilingLight(SwitchbotDevice):
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

    def command_set_brightness(self, value: int) -> str:
        """
        * value 0~100
        """
        return json.dumps({
            "command": "setBrightness",
            "commandType": "command",
            "parameter": value,
        })

    def command_set_color(self, r: int, g: int, b: int) -> str:
        """
        * r/g/b 0~255
        """
        return json.dumps({
            "command": "setColor",
            "commandType": "command",
            "parameter": f"{r}:{g}:{b}",
        })

    def command_set_color_temperature(self, value: int) -> str:
        """
        * value 2700~6500
        """
        return json.dumps({
            "command": "setColorTemperature",
            "commandType": "command",
            "parameter": value,
        })


class CeilingLightPro(CeilingLight):
    pass


class Plug(SwitchbotDevice):
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


class PlugMiniUS(Plug):
    def command_toggle(self) -> str:
        return json.dumps({
            "command": "toggle",
            "commandType": "command",
            "parameter": "default",
        })


class PlugMiniJP(PlugMiniUS):
    pass


class StripLight(SwitchbotDevice):
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

    def command_set_brightness(self, value: int) -> str:
        """
        * value 0~100
        """
        return json.dumps({
            "command": "setBrightness",
            "commandType": "command",
            "parameter": value,
        })

    def command_set_color(self, r: int, g: int, b: int) -> str:
        """
        * r/g/b 0~255
        """
        return json.dumps({
            "command": "setColor",
            "commandType": "command",
            "parameter": f"{r}:{g}:{b}",
        })


class ColorBulb(StripLight):
    def command_set_color_temperature(self, value: int) -> str:
        """
        * value 2700~6500
        """
        return json.dumps({
            "command": "setColorTemperature",
            "commandType": "command",
            "parameter": value,
        })


class RobotVacuumCleanerS1(SwitchbotDevice):
    def command_start(self) -> str:
        return json.dumps({
            "command": "start",
            "commandType": "command",
            "parameter": "default",
        })

    def command_stop(self) -> str:
        return json.dumps({
            "command": "stop",
            "commandType": "command",
            "parameter": "default",
        })

    def command_dock(self) -> str:
        return json.dumps({
            "command": "dock",
            "commandType": "command",
            "parameter": "default",
        })

    def command_pow_level(self, level: int) -> str:
        """
        * level
        0: quiet
        1: standard
        2: strong
        3: max
        """
        return json.dumps({
            "command": "PowLevel",
            "commandType": "command",
            "parameter": level,
        })


class RobotVacuumCleanerS1Plus(RobotVacuumCleanerS1):
    pass


class Humidifier(SwitchbotDevice):
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

    def command_set_mode(self, mode: str) -> str:
        """
        * mode
        auto: Auto Mode
        101: set atomization efficiency to 34%
        102: set atomization efficiency to 67%
        103: set atomization efficiency to 100%
        0~100: set atomization efficiency
        """
        return json.dumps({
            "command": "setMode",
            "commandType": "command",
            "parameter": mode,
        })
