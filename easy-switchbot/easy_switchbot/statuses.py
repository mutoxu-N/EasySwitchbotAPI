
class Status:
    """The parent class of statuses
    """

    def __init__(
            self,
            device_id: str,
            version: str,
            hub_device_id: str) -> None:
        self._device_id = device_id
        self._version = version
        self._hub_device_id = hub_device_id

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(id: {self.device_id}, version: {self.version})"

    def __repr__(self) -> str:
        return str(self)

    @property
    def device_id(self) -> str: return self._device_id
    @property
    def hub_device_id(self) -> str: return self._hub_device_id
    @property
    def version(self) -> str: return self._version


class BatteriedStatus(Status):
    def __init__(
            self,
            device_id: str,
            version: str,
            battery: int,
            hub_device_id: str) -> None:
        super().__init__(device_id, version, hub_device_id)
        self._battery = battery

    @property
    def battery(self) -> int:
        """
        battery level, 0-100
        """
        return self._battery


class BotStatus(BatteriedStatus):
    def __init__(
            self,
            device_id: str,
            power: str,
            battery: int,
            version: str,
            device_mode: str,
            hub_device_id: str) -> None:
        super().__init__(device_id, version, battery, hub_device_id)
        self._power = power
        self._device_mode = device_mode

    @property
    def power(self) -> str:
        """
        on / off
        """
        return self._power

    @property
    def device_mode(self) -> str:
        """
        pressMode/switchMode/customizeMode
        """
        return self._device_mode


class CurtainStatus(BatteriedStatus):
    def __init__(
            self,
            device_id: str,
            hub_device_id: str,
            calibrate: bool,
            group: bool,
            moving: bool,
            battery: int,
            version: str,
            slidePosition: str,) -> None:
        super().__init__(device_id, version, battery, hub_device_id)
        self._calibrate = calibrate
        self._group = group
        self._moving = moving
        self._slidePosition = slidePosition

    @property
    def calibrate(self) -> bool: return self._calibrate
    @property
    def group(self) -> bool: return self._group
    @property
    def moving(self) -> str: return self._moving

    @property
    def slidePosition(self) -> str:
        """
        the percentage of the distance
        """
        return self._slidePosition


class Curtain3Status(CurtainStatus):
    pass


class MeterStatus(BatteriedStatus):
    def __init__(
            self,
            device_id: str,
            hub_device_id: str,
            temperature: float,
            version: str,
            battery: int,
            humidity: int) -> None:
        super().__init__(device_id, version, battery, hub_device_id)
        self._temperature = temperature
        self._humidity = humidity

    @property
    def temperature(self) -> float: return self._temperature
    @property
    def humidity(self) -> int: return self._humidity


class MeterPlusStatus(MeterStatus):
    pass


class OutdoorMeterStatus(MeterStatus):
    pass


class LockStatus(BatteriedStatus):
    def __init__(
            self,
            device_id: str,
            hub_device_id: str,
            battery: int,
            version: str,
            lock_state: str,
            door_state: str,
            calibrate: bool,) -> None:
        super().__init__(device_id, version, battery, hub_device_id)

        self._lock_state = lock_state
        self._door_state = door_state
        self._calibrate = calibrate

    @property
    def lock_state(self) -> str: return self._lock_state
    @property
    def door_state(self) -> str: return self._door_state
    @property
    def calibrate(self) -> bool: return self._calibrate


class KeypadStatus(Status):
    def __init__(
            self,
            device_id: str,
            hub_device_id: str) -> None:
        super().__init__(device_id, None, hub_device_id)


class KeypadTouchStatus(KeypadStatus):
    pass


class MotionSensorStatus(BatteriedStatus):
    def __init__(
            self,
            device_id: str,
            hub_device_id: str,
            battery: int,
            version: str,
            move_detected: bool,
            brightness: str,) -> None:
        super().__init__(device_id, version, battery, hub_device_id)

        self._move_detected = move_detected
        self._brightness = brightness

    @property
    def move_detected(self) -> bool: return self._move_detected

    @property
    def brightness(self) -> str:
        """
        bright or dim
        """
        return self._brightness


class ContactSensorStatus(MotionSensorStatus):
    def __init__(
            self,
            device_id: str,
            hub_device_id: str,
            battery: int,
            version: str,
            move_detected: bool,
            open_state: str,
            brightness: str,) -> None:
        super().__init__(device_id, hub_device_id,
                         battery, version, move_detected, brightness)
        self._open_state = open_state

    @property
    def open_state(self) -> str:
        """
        open/close/timeOutNotClose
        """
        return self._open_state


class CeilingLightStatus(Status):
    def __init__(
            self,
            device_id: str,
            hub_device_id: str,
            power: str,
            version: str,
            brightness: int,
            color_temperature: int,) -> None:
        super().__init__(device_id, version, hub_device_id)

        self._power = power
        self._brightness = brightness
        self._color_temperature = color_temperature

    @property
    def power(self) -> str: return self._power

    @property
    def brightness(self) -> int:
        """
        1~100
        """
        return self._brightness

    @property
    def color_temperature(self) -> int:
        """
        2700~6500
        """
        return self._color_temperature


class CeilingLightProStatus(CeilingLightStatus):
    pass


class PlugMiniUSStatus(Status):
    def __init__(
            self,
            device_id: str,
            hub_device_id: str,
            voltage: float,
            version: str,
            weight: float,
            electricity_of_day: int,
            electric_current: float,) -> None:
        super().__init__(device_id, version, hub_device_id)
        self._voltage = voltage
        self._weight = weight
        self._electricity_of_day = electricity_of_day
        self._electric_current = electric_current

    @property
    def voltage(self) -> float: return self._voltage

    @property
    def weight(self) -> float:
        """wattage
        """
        return self._weight

    @property
    def electricity_of_day(self) -> int: return self._electricity_of_day

    @property
    def electric_current(self) -> float:
        """amps
        """
        return self._electric_current


class PlugMiniJPStatus(PlugMiniUSStatus):
    pass


class PlugStatus(Status):
    def __init__(
            self,
            device_id: str,
            power: str,
            version: str,
            hub_device_id: str,) -> None:
        super().__init__(device_id, version, hub_device_id)
        self._power = power

    @property
    def power(self) -> str: return self._power


class StripLightStatus(Status):
    def __init__(
            self,
            device_id: str,
            hub_device_id: str,
            power: str,
            version: str,
            brightness: int,
            color: str) -> None:
        super().__init__(device_id, version, hub_device_id)

        self._power = power
        self._brightness = brightness
        self._color = tuple(color.split(":"))

    @property
    def power(self) -> str: return self._power

    @property
    def brightness(self) -> int:
        """
        1~100
        """
        return self._brightness

    @property
    def color(self) -> tuple:
        """
        tuple of RGB(0~255)
        e.g. (255, 255, 255)
        """
        return self._color


class ColorBulbStatus(StripLightStatus):
    def __init__(
            self,
            device_id: str,
            hub_device_id: str,
            power: str,
            brightness: int,
            version: str,
            color: str,
            color_temperature: int) -> None:
        super().__init__(device_id, hub_device_id, power, version, brightness, color)
        self._color_temperature = color_temperature

    @property
    def color_temperature(self) -> int: return self.color_temperature


class RobotVacuumCleanerS1Status(BatteriedStatus):
    def __init__(
            self,
            device_id: str,
            hub_device_id: str,
            working_status: str,
            online_status: str,
            battery: int) -> None:
        super().__init__(device_id, None, battery, hub_device_id)

        self._working_status = working_status
        self._online_status = online_status

    @property
    def working_status(self) -> str:
        """
        * Working Status
        StandBy
        Clearing
        Paused
        GotoChargeBase
        Charging
        ChargeDone
        Dormant
        InTrouble
        InRemoteControl
        InDustCollecting
        """
        return self._working_status

    @property
    def online_status(self) -> str:
        """
        online or offline
        """
        return self._online_status


class RobotVacuumCleanerS1PlusStatus(RobotVacuumCleanerS1Status):
    def __init__(
            self,
            device_id: str,
            device_name: str,
            hub_device_id: str,
            working_status: str,
            online_status: str,
            battery: int) -> None:
        super().__init__(device_id, hub_device_id, working_status, online_status, battery)
        self._device_name = device_name

    @property
    def device_name(self) -> str: return self._device_name


class HumidifierStatus(Status):
    def __init__(
            self,
            device_id: str,
            hub_device_id: str,
            power: str,
            humidity: int,
            temperature: float,
            nebulization_efficiency: int,
            auto: bool,
            child_lock: bool,
            sound: bool,
            lack_water: bool) -> None:
        super().__init__(device_id, None, hub_device_id)

        self._power = power
        self._humidity = humidity
        self._temperature = temperature
        self._nebulization_efficiency = nebulization_efficiency
        self._auto = auto
        self._child_lock = child_lock
        self._sound = sound
        self._lack_water = lack_water

    def power(self) -> str: return self._power
    def humidity(self) -> int: return self._humidity
    def temperature(self) -> float: return self._temperature

    def nebulization_efficiency(self) -> int:
        """
        atomization efficiency percentage
        """
        return self._nebulization_efficiency

    def auto(self) -> bool: return self._auto
    def child_lock(self) -> bool: return self._child_lock
    def sound(self) -> bool: return self._sound
    def lack_water(self) -> bool: return self._lack_water


class BlindTiltStatus(Status):
    def __init__(
            self,
            device_id: str,
            hub_device_id: str,
            version: int,
            calibrate: bool,
            group: bool,
            moving: bool,
            direction: str,
            slide_position: int) -> None:
        super().__init__(device_id, version, hub_device_id)
        self._calibrate = calibrate
        self._group = group
        self._moving = moving
        self._direction = direction
        self._slide_position = slide_position

    @property
    def calibrate(self) -> bool: return self._calibrate
    @property
    def group(self) -> bool: return self._group
    @property
    def moving(self) -> bool: return self._moving
    @property
    def direction(self) -> str: return self._direction

    @property
    def slide_position(self) -> int:
        """
        0~100
        """
        return self._slide_position


class Hub2Status(Status):
    def __init__(
            self,
            device_id: str,
            hub_device_id: str,
            temperature: float,
            light_level: int,
            version: int,
            humidity: int,) -> None:
        super().__init__(device_id, version, hub_device_id)

        self._temperature = temperature
        self._light_level = light_level
        self._humidity = humidity

    @property
    def temperature(self) -> float:
        """
        temperature in celsius
        """
        return self._temperature

    @property
    def light_level(self) -> float:
        """
        1~20
        """
        return self._light_level

    @property
    def humidity(self) -> float: return self._humidity


class BatteryCirculatorFanStatus(BatteriedStatus):
    def __init__(
            self,
            device_id: str,
            device_name: str,
            mode: str,
            version: str,
            battery: int,
            power: str,
            night_status: int,
            oscillation: str,
            vertical_oscillation: str,
            charging_status: str,
            fan_speed: int,) -> None:
        super().__init__(device_id, version, battery, None)

        self._device_name = device_name
        self._mode = mode
        self._power = power
        self._night_status = night_status
        self._oscillation = oscillation
        self._vertical_oscillation = vertical_oscillation
        self._charging_status = charging_status
        self._fan_speed = fan_speed

    @property
    def device_name(self) -> str: return self._device_name

    @property
    def mode(self) -> str:
        """
        direct mode: direct
        natural mode: natural
        sleep mode: sleep
        ultra quiet mode: baby
        """
        return self._mode

    @property
    def power(self) -> str: return self._power

    @property
    def night_status(self) -> int:
        """
        off: off
        mode 1: 1
        mode 2: 2
        """
        return self._night_status

    @property
    def oscillation(self) -> str: return self._oscillation
    @property
    def vertical_oscillation(self) -> str: return self._vertical_oscillation

    @property
    def charging_status(self) -> str:
        """
        charging or uncharged
        """
        return self._charging_status

    @property
    def fan_speed(self) -> int:
        """
        0~100
        """
        return self._fan_speed
