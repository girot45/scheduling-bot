from datetime import date
from typing import Optional, List, Union
from pydantic import BaseModel


class Table(BaseModel):
    id: int
    tg_id: int
    day_of_week: int
    date: str
    timestart: str
    timeend: str
    event: str
    isrepeat: int
