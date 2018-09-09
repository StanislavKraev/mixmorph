import enum
from datetime import datetime

from dataclasses import dataclass
from decimal import Decimal


class OrderStatus(enum.Enum):
    created = 'created'
    processing = 'processing'
    delivered = 'delivered'
    cancelled = 'cancelled'


@dataclass
class OrderInfo:
    product_id: int
    quantity: int
    price: Decimal
    client_id: int
    location_id: int

    place_time: datetime
    status: OrderStatus
