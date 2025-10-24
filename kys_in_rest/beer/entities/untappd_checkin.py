from pydantic import BaseModel


class UntappdCheckin(BaseModel):
    id: int
    beer_url: str
    beer_img: str
    beer_name: str
    beer_brewery: str
    beer_brewery_url: str
    checkin_location: str
    checkin_location_url: str
    checkin_comment: str
    checkin_rating: float
    checkin_date: str
