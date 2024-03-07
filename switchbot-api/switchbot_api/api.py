import hmac
import hashlib
import time
import base64
import uuid
import requests
from typing import Any, List

from switchbot_api.devices import *

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

    def run(self, device_id: str, command: str) -> dict:
        """create POST request to operate your device

        Args:
            device_id (str):the id of your device
            command (str): the parameter json of operation

        Returns:
            dict: response of POST
        """
        headers = self.__create_headers()
        res = requests.post(
            f"{ROOT_URL}/v1.1/devices/{device_id}/commands", headers=headers, data=command)
        return res.json()

    def status(self, device: SwitchbotDevice):
        res = self.get(f"devices/{device.device_id}/status")
        if not "statusCode" in res.keys() and res["statusCode"] != 100:
            print(f"Connection failed! (Code: {int(res['statusCode'])})")
            return None
        return res["body"]

    @property
    def devices(self) -> List[SwitchbotDevice]:
        ret = []

        json = self.get("devices")

        if not "statusCode" in json.keys() and json["statusCode"] != 100:
            print(f"Connection failed! (Code: {int(json['statusCode'])})")
            return

        devices = json["body"]["deviceList"]

        for device in devices:
            # detect the device type
            if device["deviceType"] == "Plug Mini (JP)":
                ret.append(PlugMiniJP(
                    device_id=device["deviceId"],
                    device_name=device["deviceName"],
                    enable_cloud_service=device["enableCloudService"],
                    hub_device_id=device["hubDeviceId"],
                ))

        return tuple(ret)
