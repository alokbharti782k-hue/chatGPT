from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class IoTReading:
    device_id: str
    sensor: str
    value: float
    unit: str


class IoTGateway:
    """Safe boundary for future MSS/IoT integration.

    Reads may be supplied by a deterministic gateway. Actuation is intentionally
    absent here so an LLM cannot directly trigger physical side effects.
    """

    def __init__(self) -> None:
        self._readings: dict[str, IoTReading] = {}

    def record_reading(self, reading: IoTReading) -> None:
        self._readings[f"{reading.device_id}:{reading.sensor}"] = reading

    def get_reading(self, device_id: str, sensor: str) -> IoTReading | None:
        return self._readings.get(f"{device_id}:{sensor}")
