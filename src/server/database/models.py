from typing import Annotated
from datetime import datetime, UTC
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import String, Float, DateTime, ForeignKey
from . import Base


class Market(Base):
    """
    Trading market, so we could be trading for Apple OTC, or Microsoft stocks,
    Forex, Commodities etc.
    """

    __tablename__ = "markets"

    name: Mapped[int] = mapped_column(String(50), primary_key=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=lambda: datetime.now(UTC)
    )


class Candle(Base):
    """
    Each candle

    interval: how long is this candle? 10s, 60s?
    """

    __tablename__ = "candles"

    market_name: Mapped[int] = mapped_column(
        ForeignKey("markets.name"), primary_key=True
    )
    interval: Mapped[float] = mapped_column(Float)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=lambda: datetime.now(UTC)
    )

    open: Mapped[float] = mapped_column(Float)
    high: Mapped[float] = mapped_column(Float)
    low: Mapped[float] = mapped_column(Float)
    close: Mapped[float] = mapped_column(Float)
