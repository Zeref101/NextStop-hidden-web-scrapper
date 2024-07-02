from bs4 import BeautifulSoup
import requests
from fastapi import APIRouter
from app.services.location_of_places import get_location_type
from app.services.get_places_by_place_name import find_places_in_place_name
from app.services.get_places_by_state_name import find_places_in_state_name
from app.services.get_places_by_country_name import find_places_in_country_name

import re

router = APIRouter()


@router.get("/places/{location}")
async def get_places_to_visit(location: str):

    location_details = get_location_type(location)

    if location_details.get("city_rural_urban_county"):
        return find_places_in_place_name(location)

    if location_details.get("state"):
        return find_places_in_state_name(location)

    if location_details.get("country"):
        return find_places_in_country_name(location)

    return {"error": "Location not found"}
