from pydantic import BaseModel, Field, model_validator
from datetime import datetime, timedelta
from typing import Optional


class FlightInfo(BaseModel):
    name: str
    date_of_birth: str
    image_url: str


class BarInfo(BaseModel):
    image_url: str
    date_of_birth: str
    is_drinking_age: Optional[bool] = None

    @model_validator(mode='before')
    @classmethod
    def set_drinking_age(cls, values):
        dob = datetime.strptime(values['date_of_birth'], '%Y-%m-%d')
        values['is_drinking_age'] = (datetime.now() - dob) >= timedelta(days=18*365)
        return values


def get_model_for_service(service_type, data):
    if service_type == 'Flight':
        return FlightInfo(**data).model_dump()
    elif service_type == 'Bar':
        return BarInfo(**data).model_dump(exclude={'date_of_birth'})
    else:
        raise ValueError("Invalid service type")
