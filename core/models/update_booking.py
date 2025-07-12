from datetime import date
from pydantic import BaseModel
from typing import Optional


class BookingDates(BaseModel):
    checkin: date
    checkout: date

class BookingModel(BaseModel):
    firstname: str
    lastname: str
    totalprice: int
    depositpaid: bool
    bookingdates: BookingDates
    additionalneeds: str