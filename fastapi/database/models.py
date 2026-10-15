from datetime import datetime, timezone
from enum import Enum
from sqlmodel import Field, SQLModel


class ShipmentStatus(str, Enum):
    placed = "placed"
    delivered = "delivered"
    in_transit = "in_transit"
    cancelled = "cancelled"
    pending = "pending"
    shipped = "shipped"


class Shipment(SQLModel, table=True):
    __tablename__ = "shipments"

    id: int | None = Field(default=None, primary_key=True)
    content: str
    weight: float = Field(ge=0, le=20)
    expected_delivery: datetime
    destination: str
    status: ShipmentStatus = Field(default=ShipmentStatus.placed)


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(unique=True, index=True)
    email: str = Field(unique=True, index=True)
    password_hash: str


# stores revoked tokens when user logs out
class RevokedToken(SQLModel, table=True):
    __tablename__ = "revoked_tokens"

    id: int | None = Field(default=None, primary_key=True)
    token: str = Field(unique=True, index=True)
    revoked_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
