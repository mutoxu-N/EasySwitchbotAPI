import hmac
import hashlib
import time
import base64
import uuid
import requests
from typing import List

from easy_switchbot.devices import *
from easy_switchbot.infrared_devices import *
from easy_switchbot.statuses import *
from easy_switchbot.types import Command

ROOT_URL = "https://api.switch-bot.com"


class SwitchbotAPI:
    """The class which accesses API.
    """

    def __init__(self, token: str, secret: str) -> None:
        """the constructor for SwitchbotAPI

        Args:
            token (str): access token (getting from mobile app)
            secret (str): secret key (getting from mobile app)
        """
        self._token: str = token
        self._secret: bytes = bytes(secret, "utf-8")

    def __create_headers(self) -> dict:
        """creating the header for authorization.

        Returns:
            dict: headers
        """
        time_ = str(int(round(time.time()*1000)))
        nonce = str(uuid.uuid4())

        sign = base64.b64encode(
            hmac.new(
                key=self._secret,
                msg=bytes(f"{self._token}{time_}{nonce}", "utf-8"),
                digestmod=hashlib.sha256).digest()
        )

        return {
            "Authorization": self._token,
            "sign": sign,
            "t": time_,
            "nonce": nonce,
            "Content-Type": "application/json; charset=utf-8"
        }

    def __is_success(self, res: dict) -> bool:
        if not "statusCode" in res.keys() or res["statusCode"] != 100:
            print(f"Connection failed!")
            return False
        return True

    def get(self, path: str) -> dict:
        """create GET request to API.
            * Access to the \"{ROOT_URL}/v1.1/{path}\" and return a response.

        Args:
            path (str): segment of URL

        Returns:
            dict: response of GET
        """
        headers = self.__create_headers()
        res = requests.get(
            f"{ROOT_URL}/v1.1/{path}", headers=headers)

        return res.json()

    def run(self, command: Command) -> dict:
        """create POST request to operate your device

        Args:
            command (Command): command generated from \"command_***()\" function

        Returns:
            dict: json response of POST
        """
        headers = self.__create_headers()
        res = requests.post(
            f"{ROOT_URL}/v1.1/devices/{command.device_id}/commands", headers=headers, data=command.command)
        return res.json()

    def status(self, device: SwitchbotDevice) -> Status:
        res = self.get(f"devices/{device.device_id}/status")

        if not self.__is_success(res):
            raise ConnectionError("response: " + str(res))

        data = res["body"]

        if data["deviceType"] == "Bot":
            return BotStatus(
                device_id=data["deviceId"],
                power=data["power"],
                battery=data["battery"],
                version=data["version"],
                device_mode=data["deviceMode"],
                hub_device_id=data["hubDeviceId	"],
            )
        elif data["deviceType"] == "Curtain":
            return CurtainStatus(
                device_id=data["deviceId"],
                hub_device_id=data["hubDeviceId"],
                calibrate=data["calibrate"],
                group=data["group"],
                moving=data["moving"],
                battery=data["battery"],
                version=data["version"],
                slidePosition=data["slidePosition"],
            )
        elif data["deviceType"] == "Curtain3":
            return Curtain3Status(
                device_id=data["deviceId"],
                hub_device_id=data["hubDeviceId"],
                calibrate=data["calibrate"],
                group=data["group"],
                moving=data["moving"],
                battery=data["battery"],
                version=data["version"],
                slidePosition=data["slidePosition"],
            )
        elif data["deviceType"] == "Meter":
            return MeterStatus(
                device_id=data["deviceId"],
                hub_device_id=data["hubDeviceId"],
                temperature=data["temperature"],
                version=data["version"],
                battery=data["battery"],
                humidity=data["humidity"]
            )
        elif data["deviceType"] == "MeterPlus":
            return MeterPlusStatus(
                device_id=data["deviceId"],
                hub_device_id=data["hubDeviceId"],
                temperature=data["temperature"],
                version=data["version"],
                battery=data["battery"],
                humidity=data["humidity"]
            )
        elif data["deviceType"] == "WoIOSensor":
            return OutdoorMeterStatus(
                device_id=data["deviceId"],
                hub_device_id=data["hubDeviceId"],
                temperature=data["temperature"],
                version=data["version"],
                battery=data["battery"],
                humidity=data["humidity"]
            )
        elif data["deviceType"] == "Smart Lock":
            return LockStatus(
                device_id=data["deviceId"],
                hub_device_id=data["hubDeviceId"],
                battery=data["battery"],
                version=data["version"],
                lock_state=data["lockState"],
                door_state=data["doorState"],
                calibrate=data["calibrate"],
            )
        elif data["deviceType"] == "Keypad":
            return KeypadStatus(
                device_id=data["deviceId"],
                hub_device_id=data["hubDeviceId"],
            )
        elif data["deviceType"] == "Keypad Touch":
            return KeypadTouchStatus(
                device_id=data["deviceId"],
                hub_device_id=data["hubDeviceId"],
            )
        elif data["deviceType"] == "Motion Sensor":
            return MotionSensorStatus(
                device_id=data["deviceId"],
                hub_device_id=data["hubDeviceId"],
                battery=data["battery"],
                version=data["version"],
                move_detected=data["moveDetected"],
                brightness=data["brightness"],
            )
        elif data["deviceType"] == "Contact Sensor":
            return MotionSensorStatus(
                device_id=data["deviceId"],
                hub_device_id=data["hubDeviceId"],
                battery=data["battery"],
                version=data["version"],
                move_detected=data["moveDetected"],
                open_state=data["openState"],
                brightness=data["brightness"],
            )
        elif data["deviceType"] == "Ceiling Light":
            return CeilingLightStatus(
                device_id=data["deviceId"],
                hub_device_id=data["hubDeviceId"],
                power=data["power"],
                version=data["version"],
                brightness=data["brightness"],
                color_temperature=data["colorTemperature"],
            )
        elif data["deviceType"] == "Ceiling Light Pro":
            return CeilingLightProStatus(
                device_id=data["deviceId"],
                hub_device_id=data["hubDeviceId"],
                power=data["power"],
                version=data["version"],
                brightness=data["brightness"],
                color_temperature=data["colorTemperature"],
            )
        elif data["deviceType"] == "Plug Mini (US)":
            return PlugMiniUSStatus(
                device_id=data["deviceId"],
                hub_device_id=data["hubDeviceId"],
                voltage=data["voltage"],
                version=data["version"],
                weight=data["weight"],
                electricity_of_day=data["electricityOfDay"],
                electric_current=data["electricCurrent"],
            )
        elif data["deviceType"] == "Plug Mini (JP)":
            return PlugMiniJPStatus(
                device_id=data["deviceId"],
                hub_device_id=data["hubDeviceId"],
                voltage=data["voltage"],
                version=data["version"],
                weight=data["weight"],
                electricity_of_day=data["electricityOfDay"],
                electric_current=data["electricCurrent"],
            )
        elif data["deviceType"] == "Plug":
            return PlugStatus(
                device_id=data["deviceId"],
                hub_device_id=data["hubDeviceId"],
                power=data["power"],
                version=data["version"],
            )
        elif data["deviceType"] == "Strip Light":
            return StripLightStatus(
                device_id=data["deviceId"],
                hub_device_id=data["hubDeviceId"],
                power=data["power"],
                version=data["version"],
                brightness=data["brightness"],
                color=data["color"]
            )
        elif data["deviceType"] == "Color Bulb":
            return ColorBulbStatus(
                device_id=data["deviceId"],
                hub_device_id=data["hubDeviceId"],
                power=data["power"],
                version=data["version"],
                brightness=data["brightness"],
                color=data["color"],
                color_temperature=data["colorTemperature"]
            )
        elif data["deviceType"] == "Robot Vacuum Cleaner S1":
            return RobotVacuumCleanerS1Status(
                device_id=data["deviceId"],
                hub_device_id=data["hubDeviceId"],
                working_status=data["workingStatus"],
                online_status=data["onlineStatus"],
                battery=data["battery"]
            )
        elif data["deviceType"] == "Robot Vacuum Cleaner S1 Plus":
            return RobotVacuumCleanerS1PlusStatus(
                device_id=data["deviceId"],
                device_name=data["deviceName"],
                hub_device_id=data["hubDeviceId"],
                working_status=data["workingStatus"],
                online_status=data["onlineStatus"],
                battery=data["battery"]
            )
        elif data["deviceType"] == "Humidifier":
            return HumidifierStatus(
                device_id=data["deviceId"],
                hub_device_id=data["hubDeviceId"],
                power=data["power"],
                humidity=data["humidity"],
                temperature=data["temperature"],
                nebulization_efficiency=data["nebulizationEfficiency"],
                auto=data["auto"],
                child_lock=data["childLock"],
                sound=data["sound"],
                lack_water=data["lackWater"],
            )
        elif data["deviceType"] == "Blind Tilt":
            return BlindTiltStatus(
                device_id=data["deviceId"],
                hub_device_id=data["hubDeviceId"],
                version=data["version"],
                calibrate=data["calibrate"],
                group=data["group"],
                moving=data["moving"],
                direction=data["direction"],
                slide_position=data["slidePosition"],
            )
        elif data["deviceType"] == "Hub 2":
            return Hub2Status(
                device_id=data["deviceId"],
                hub_device_id=data["hubDeviceId"],
                temperature=data["temperature"],
                light_level=data["lightLevel"],
                version=data["version"],
                humidity=data["humidity"],
            )
        elif data["deviceType"] == "Battery Circulator Fan":
            return BatteryCirculatorFanStatus(
                device_id=data["deviceId"],
                device_name=data["deviceName"],
                mode=data["mode"],
                version=data["version"],
                battery=data["battery"],
                power=data["power"],
                night_status=data["nightStatus"],
                oscillation=data["oscillation"],
                vertical_oscillation=data["verticalOscillation"],
                charging_status=data["chargingStatus"],
                fan_speed=data["fanSpeed"],
            )

    @property
    def devices(self) -> List[Device]:
        ret = []

        json = self.get("devices")

        if not self.__is_success(json):
            raise ConnectionError("response: " + str(json))

        devices = json["body"]["deviceList"]

        for device in devices:
            # detect the device type
            if device["deviceType"] == "Bot":
                ret.append(Bot(
                    device_id=device["deviceId"],
                    device_name=device["deviceName"],
                    enable_cloud_service=device["enableCloudService"],
                    hub_device_id=device["hubDeviceId"],
                ))
            elif device["deviceType"] == "Curtain":
                ret.append(Curtain(
                    device_id=device["deviceId"],
                    device_name=device["deviceName"],
                    enable_cloud_service=device["enableCloudService"],
                    hub_device_id=device["hubDeviceId"],
                    curtain_device_ids=device["curtainDevicesIds"],
                    calibrate=device["calibrate"],
                    group=device["group"],
                    master=device["master"],
                    openDirection=device["openDirection"]
                ))
            elif device["deviceType"] == "Curtain3":
                ret.append(Curtain3(
                    device_id=device["deviceId"],
                    device_name=device["deviceName"],
                    enable_cloud_service=device["enableCloudService"],
                    hub_device_id=device["hubDeviceId"],
                    curtain_device_ids=device["curtainDevicesIds"],
                    calibrate=device["calibrate"],
                    group=device["group"],
                    master=device["master"],
                    openDirection=device["openDirection"]
                ))
            elif device["deviceType"] == "Hub":
                ret.append(Hub(
                    device_id=device["deviceId"],
                    device_name=device["deviceName"],
                    enable_cloud_service=device["enableCloudService"],
                    hub_device_id=device["hubDeviceId"],
                ))
            elif device["deviceType"] == "Hub Plus":
                ret.append(HubPlus(
                    device_id=device["deviceId"],
                    device_name=device["deviceName"],
                    enable_cloud_service=device["enableCloudService"],
                    hub_device_id=device["hubDeviceId"],
                ))
            elif device["deviceType"] == "Hub Mini":
                ret.append(HubMini(
                    device_id=device["deviceId"],
                    device_name=device["deviceName"],
                    enable_cloud_service=device["enableCloudService"],
                    hub_device_id=device["hubDeviceId"],
                ))
            elif device["deviceType"] == "Hub 2":
                ret.append(Hub2(
                    device_id=device["deviceId"],
                    device_name=device["deviceName"],
                    enable_cloud_service=device["enableCloudService"],
                    hub_device_id=device["hubDeviceId"],
                ))
            elif device["deviceType"] == "Meter":
                ret.append(Meter(
                    device_id=device["deviceId"],
                    device_name=device["deviceName"],
                    enable_cloud_service=device["enableCloudService"],
                    hub_device_id=device["hubDeviceId"],
                ))
            elif device["deviceType"] == "MeterPlus":
                ret.append(MeterPlus(
                    device_id=device["deviceId"],
                    device_name=device["deviceName"],
                    enable_cloud_service=device["enableCloudService"],
                    hub_device_id=device["hubDeviceId"],
                ))
            elif device["deviceType"] == "WoIOSensor":
                ret.append(OutdoorMeter(
                    device_id=device["deviceId"],
                    device_name=device["deviceName"],
                    enable_cloud_service=device["enableCloudService"],
                    hub_device_id=device["hubDeviceId"],
                ))
            elif device["deviceType"] == "Smart Lock":
                ret.append(Lock(
                    device_id=device["deviceId"],
                    device_name=device["deviceName"],
                    enable_cloud_service=device["enableCloudService"],
                    hub_device_id=device["hubDeviceId"],
                    group=device["group"],
                    master=device["master"],
                    group_name=device["groupName"],
                    lock_device_ids=device["lockDevicesIds"],
                ))
            elif device["deviceType"] == "Keypad":
                ret.append(Keypad(
                    device_id=device["deviceId"],
                    device_name=device["deviceName"],
                    enable_cloud_service=device["enableCloudService"],
                    hub_device_id=device["hubDeviceId"],
                ))
            elif device["deviceType"] == "Keypad Touch":
                ret.append(KeypadTouch(
                    device_id=device["deviceId"],
                    device_name=device["deviceName"],
                    enable_cloud_service=device["enableCloudService"],
                    hub_device_id=device["hubDeviceId"],
                    lock_device_id=device["lockDeviceId"],
                    key_list=device["keyList"],
                ))
            elif device["deviceType"] == "Remote":
                ret.append(Remote(
                    device_id=device["deviceId"],
                    device_name=device["deviceName"],
                    enable_cloud_service=device["enableCloudService"],
                    hub_device_id=device["hubDeviceId"],
                ))
            elif device["deviceType"] == "Motion Sensor":
                ret.append(MotionSensor(
                    device_id=device["deviceId"],
                    device_name=device["deviceName"],
                    enable_cloud_service=device["enableCloudService"],
                    hub_device_id=device["hubDeviceId"],
                ))
            elif device["deviceType"] == "Contact Sensor":
                ret.append(ContactSensor(
                    device_id=device["deviceId"],
                    device_name=device["deviceName"],
                    enable_cloud_service=device["enableCloudService"],
                    hub_device_id=device["hubDeviceId"],
                ))
            elif device["deviceType"] == "Ceiling Light":
                ret.append(CeilingLight(
                    device_id=device["deviceId"],
                    device_name=device["deviceName"],
                    enable_cloud_service=device["enableCloudService"],
                    hub_device_id=device["hubDeviceId"],
                ))
            elif device["deviceType"] == "Ceiling Light Pro":
                ret.append(CeilingLightPro(
                    device_id=device["deviceId"],
                    device_name=device["deviceName"],
                    enable_cloud_service=device["enableCloudService"],
                    hub_device_id=device["hubDeviceId"],
                ))
            elif device["deviceType"] == "Plug":
                ret.append(Plug(
                    device_id=device["deviceId"],
                    device_name=device["deviceName"],
                    enable_cloud_service=device["enableCloudService"],
                    hub_device_id=device["hubDeviceId"],
                ))
            elif device["deviceType"] == "Plug Mini (US)":
                ret.append(PlugMiniUS(
                    device_id=device["deviceId"],
                    device_name=device["deviceName"],
                    enable_cloud_service=device["enableCloudService"],
                    hub_device_id=device["hubDeviceId"],
                    lock_device_id=device["lockDeviceId"],
                    key_list=device["keyList"],
                ))
            elif device["deviceType"] == "Plug Mini (JP)":
                ret.append(PlugMiniJP(
                    device_id=device["deviceId"],
                    device_name=device["deviceName"],
                    enable_cloud_service=device["enableCloudService"],
                    hub_device_id=device["hubDeviceId"],
                ))
            elif device["deviceType"] == "Strip Light":
                ret.append(StripLight(
                    device_id=device["deviceId"],
                    device_name=device["deviceName"],
                    enable_cloud_service=device["enableCloudService"],
                    hub_device_id=device["hubDeviceId"],
                ))
            elif device["deviceType"] == "Color Bulb":
                ret.append(ColorBulb(
                    device_id=device["deviceId"],
                    device_name=device["deviceName"],
                    enable_cloud_service=device["enableCloudService"],
                    hub_device_id=device["hubDeviceId"],
                ))
            elif device["deviceType"] == "Robot Vacuum Cleaner S1":
                ret.append(RobotVacuumCleanerS1(
                    device_id=device["deviceId"],
                    device_name=device["deviceName"],
                    enable_cloud_service=device["enableCloudService"],
                    hub_device_id=device["hubDeviceId"],
                ))
            elif device["deviceType"] == "Robot Vacuum Cleaner S1 Plus":
                ret.append(RobotVacuumCleanerS1Plus(
                    device_id=device["deviceId"],
                    device_name=device["deviceName"],
                    enable_cloud_service=device["enableCloudService"],
                    hub_device_id=device["hubDeviceId"],
                ))
            elif device["deviceType"] == "Humidifier":
                ret.append(Humidifier(
                    device_id=device["deviceId"],
                    device_name=device["deviceName"],
                    enable_cloud_service=device["enableCloudService"],
                    hub_device_id=device["hubDeviceId"],
                ))
            elif device["deviceType"] == "Indoor Cam":
                ret.append(IndoorCam(
                    device_id=device["deviceId"],
                    device_name=device["deviceName"],
                    enable_cloud_service=device["enableCloudService"],
                    hub_device_id=device["hubDeviceId"],
                ))
            elif device["deviceType"] == "Pan/Tilt Cam":
                ret.append(PanTiltCam(
                    device_id=device["deviceId"],
                    device_name=device["deviceName"],
                    enable_cloud_service=device["enableCloudService"],
                    hub_device_id=device["hubDeviceId"],
                ))
            # "Pan/Tilt Cam" in API document.
            elif device["deviceType"] == "Pan/Tilt Cam 2K":
                ret.append(PanTiltCam2K(
                    device_id=device["deviceId"],
                    device_name=device["deviceName"],
                    enable_cloud_service=device["enableCloudService"],
                    hub_device_id=device["hubDeviceId"],
                ))
            elif device["deviceType"] == "Blind Tilt":
                ret.append(BlindTilt(
                    device_id=device["deviceId"],
                    device_name=device["deviceName"],
                    enable_cloud_service=device["enableCloudService"],
                    hub_device_id=device["hubDeviceId"],
                    blind_tilt_device_ids=device["blindTiltDevicesIds"],
                    calibrate=device["calibrate"],
                    group=device["group"],
                    master=device["master"],
                    direction=device["direction"],
                    slide_position=device["slidePosition"],
                ))
            elif device["deviceType"] == "Battery Circulator Fan":
                ret.append(BatteryCirculatorFan(
                    device_id=device["deviceId"],
                    device_name=device["deviceName"],
                    enable_cloud_service=device["enableCloudService"],
                    hub_device_id=device["hubDeviceId"],
                ))

        if not "infraredRemoteList" in json["body"].keys():
            return tuple(ret)

        devices = json["body"]["infraredRemoteList"]
        for device in devices:
            if device["remoteType"] == "Air Conditioner":
                ret.append(AirConditionerInfrared(
                    device_id=device["deviceId"],
                    device_name=device["deviceName"],
                    hub_device_id=device["hubDeviceId"]
                ))
            elif device["remoteType"] == "TV":
                ret.append(TVInfrared(
                    device_id=device["deviceId"],
                    device_name=device["deviceName"],
                    hub_device_id=device["hubDeviceId"]
                ))
            elif device["remoteType"] == "IPTV/Streamer":
                ret.append(StreamerInfrared(
                    device_id=device["deviceId"],
                    device_name=device["deviceName"],
                    hub_device_id=device["hubDeviceId"]
                ))
            elif device["remoteType"] == "Set Top Box":
                ret.append(SetTopBoxInfrared(
                    device_id=device["deviceId"],
                    device_name=device["deviceName"],
                    hub_device_id=device["hubDeviceId"]
                ))
            elif device["remoteType"] == "DVD":
                ret.append(DVDInfrared(
                    device_id=device["deviceId"],
                    device_name=device["deviceName"],
                    hub_device_id=device["hubDeviceId"]
                ))
            elif device["remoteType"] == "Speaker":
                ret.append(SpeakerInfrared(
                    device_id=device["deviceId"],
                    device_name=device["deviceName"],
                    hub_device_id=device["hubDeviceId"]
                ))
            elif device["remoteType"] == "Fan":
                ret.append(FanInfrared(
                    device_id=device["deviceId"],
                    device_name=device["deviceName"],
                    hub_device_id=device["hubDeviceId"]
                ))
            elif device["remoteType"] == "Light":
                ret.append(LightInfrared(
                    device_id=device["deviceId"],
                    device_name=device["deviceName"],
                    hub_device_id=device["hubDeviceId"]
                ))
            else:
                ret.append(OtherInfrared(
                    device_id=device["deviceId"],
                    device_name=device["deviceName"],
                    remote_type=device["remoteType"],
                    hub_device_id=device["hubDeviceId"]))

        return tuple(ret)

    def get_devices(self, device_ids: List[str]) -> dict:
        """return device list from device id list
        If the devices was not founded, it returns None.

        * returns (dict)
          Key means device id. Value means Device instance.
        """
        # initialize
        ret = {}
        for id in device_ids:
            ret[id] = None

        # search all devices
        devices = self.devices
        for device in devices:
            if device.device_id in device_ids:
                ret[device.device_id] = device

        return ret
