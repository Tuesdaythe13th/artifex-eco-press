from pydantic import BaseModel, Field

class CyclePacket(BaseModel):
    cycle_id: int = Field(ge=0)
    schema_version: int = 1
    timestamp_ms: int = Field(ge=0)
    dew_point: float = Field(ge=-80, le=25)
    nir_moisture: float = Field(ge=0, le=1000)
    b_zone1_temp: float = Field(ge=0, le=320)
    b_zone2_temp: float = Field(ge=0, le=320)
    b_zone3_temp: float = Field(ge=0, le=320)
    b_zone4_temp: float = Field(ge=0, le=320)
    m_temp: float = Field(ge=20, le=120)
    close_time: float = Field(ge=3, le=6)
    inj_peak_pressure: float = Field(ge=0, le=200000)
    shot_weight: float = Field(ge=150, le=210)
    ai_haze_score: float = Field(ge=0, le=1)
    ai_flash_detected: bool
    reject_code: str
    crc16: int = Field(ge=0, le=65535)
