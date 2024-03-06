import hmac
import hashlib
import time
import base64
import uuid
import requests


class SwitchbotAPI:
    def __init__(self, token: str, secret: str) -> None:
        self._token: str = token
        self._secret: bytes = bytes(secret, "utf-8")

    def get(self, path: str) -> dict:
        time_ = str(int(round(time.time()*1000)))
        nonce = str(uuid.uuid4())

        sign = base64.b64encode(
            hmac.new(
                key=self._secret,
                msg=bytes(f"{self._token}{time_}{nonce}", "utf-8"),
                digestmod=hashlib.sha256).digest()
        )

        headers = {
            "Authorization": self._token,
            "sign": sign,
            "t": time_,
            "nonce": nonce,
            "Content-Type": "application/json; charset=utf-8"
        }

        res = requests.get(
            f"https://api.switch-bot.com/v1.1/{path}", headers=headers)

        return res.json()
