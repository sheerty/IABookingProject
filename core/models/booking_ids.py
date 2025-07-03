from pydantic import BaseModel, RootModel
from typing import Optional, List


class BookingIds(BaseModel):
    bookingid : int

class BookingResponse(RootModel):
    root: List[BookingIds]
