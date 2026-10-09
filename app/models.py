from pydantic import BaseModel, ConfigDict


class Meter(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    meter_id: str
    serial_number: str | None = None
    make: str | None = None
    phase_type: str | None = None
    installation_status: str | None = None
    dt_code: str | None = None


class MeterListResponse(BaseModel):
    data: list[Meter]
    total: int
    page: int
    page_size: int


class ConsumptionReading(BaseModel):
    timestamp: str
    kwh: float
    kvah: float
    voltage_r: float


class Location(BaseModel):
    latitude: float
    longitude: float


class MeterDetails(Meter):
    installation_type: str | None = None
    latitude: float | None = None
    longitude: float | None = None


class ConsumptionResponse(BaseModel):
    meter_id: str
    readings: list[ConsumptionReading]


class LocationResponse(BaseModel):
    meter_id: str
    location: Location
