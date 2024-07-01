from bs4 import BeautifulSoup
import requests
from fastapi import APIRouter
from app.services.location_of_places import get_location_type
from app.services.get_places_by_place_name import find_places_in_place_name
from app.services.get_places_by_state_name import find_places_in_state_name

import re

router = APIRouter()


@router.get("/places/{location}")
async def get_places_to_visit(location: str):

    location_details = get_location_type(location)

    print(location_details)

    if location_details.get("city_rural_urban_county") != None:
        res = find_places_in_place_name(location)
        return res

    elif location_details.get("city_rural_urban_county") == None and location_details.get("state") != None:
        res = find_places_in_state_name(location)
        return res
