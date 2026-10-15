from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field, EmailStr


class ShipmentStatus(str, Enum):
    placed = "placed"
    delivered = "delivered"
    in_transit = "in_transit"
    cancelled = "cancelled"
    pending = "pending"
    shipped = "shipped"


# pydantic model for creating a shipment
class Ship(BaseModel):
    weight: float = Field(gt=0, le=20)
    content: str = Field(max_length=50)
    destination: str
    expected_delivery: datetime
    status: ShipmentStatus = ShipmentStatus.placed


# for partial updates (all fields optional)
class ShipmentPatch(BaseModel):
    weight: float | None = Field(default=None, gt=0, le=20)
    content: str | None = Field(default=None, max_length=50)
    destination: str | None = None
    expected_delivery: datetime | None = None
    status: ShipmentStatus | None = None


# for complete updates
class UpdateShipment(Ship):
    pass


# simple response model used in earlier learning exercises
class Response(BaseModel):
    id: int
    status: str
    weight: float
    content: str


# user registration schema
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


# user response (never return password_hash to the client)
class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr


# login credentials payload
class LoginUser(BaseModel):
    email: EmailStr
    password: str


# response returned on successful login
class LoginResponse(BaseModel):
    message: str
    userid: int
    username: str
    email: EmailStr
    token: str
