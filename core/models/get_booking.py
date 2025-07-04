from datetime import date
from pydantic import BaseModel
from typing import Optional

class BookingDates(BaseModel):
    """Модель для дат бронирования"""
    checkin: date
    checkout: date

class BookingResponse(BaseModel):
    """Полная модель ответа с информацией о бронировании"""
    firstname: str
    lastname: str
    totalprice: int
    depositpaid: bool
    bookingdates: BookingDates
    additionalneeds: Optional[str] = None
