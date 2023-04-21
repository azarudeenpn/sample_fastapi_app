"""
Dataclass that enforces and validates schema when API requests arrives.
"""

import re

from pydantic import BaseModel, validator


class Coordinates(BaseModel):
    lat: float
    lon: float


class AddressModel(BaseModel):
    name: str
    email: str
    country: str
    coordinate: Coordinates

    @validator('email')
    def email_validator(cls, v):
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
        if re.fullmatch(regex, v.title()):
            pass
        else:
            raise ValueError('invalid email')
        return v.title()

    def to_tuple(self):
        """
        Helper method to return data ready for database operations.
        :return: tuple of serialized data.
        """
        return tuple([self.name, self.email, self.country, self.coordinate.lat, self.coordinate.lon])
