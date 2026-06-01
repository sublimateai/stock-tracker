from pydantic import BaseModel, Field


class WebSocketClientCreate(BaseModel):
    market_name: str = Field(min_length=1, max_length=50)


class CandleCreate(BaseModel):
    market_name: str = Field(min_length=1, max_length=50)
    interval: float
    open: float
    high: float
    low: float
    close: float

