
class SwitchbotDevice:
    def __init__(
            self,
            device_id: str,
            device_name: str,
            enable_cloud_service: bool,
            hub_device_id: str) -> None:

        self._device_id = device_id
        self._device_name = device_name
        self._enable_cloud_service = enable_cloud_service
        self._hub_device_id = hub_device_id

    def __str__(self) -> str:
        return f"{self.__class__.__name__} (id: {self._device_id}, name: {self._device_name})"


class PlugMiniJP(SwitchbotDevice):
    def __init__(
            self,
            device_id: str,
            device_name: str,
            enable_cloud_service: bool,
            hub_device_id: str) -> None:
        super().__init__(device_id, device_name, enable_cloud_service, hub_device_id)
