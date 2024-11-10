from bs4 import BeautifulSoup
import requests
from fastapi import APIRouter, HTTPException, Response
from app.services.location_of_places import get_location_type
from app.services.get_places_by_place_name import find_places_in_place_name
from app.services.get_places_by_state_name import find_places_in_state_name
from app.services.get_places_by_country_name import find_places_in_country_name
import os
import json
import gzip

router = APIRouter()


@router.get("/places/{location}")
async def get_places_to_visit(location: str):

    try:
        location_details = get_location_type(location)

        res = ''

        if location_details.get("city_rural_urban_county"):
            res = find_places_in_place_name(location)

        elif location_details.get("state"):
            res = find_places_in_state_name(location)

        elif location_details.get("country"):
            res = find_places_in_country_name(location)

        headers = {
            'Content-Type': 'application/json'
        }

        res_list = json.loads(res)

        res_json = json.dumps({"places_info": res_list})

        # Compress the data
        compressed_data = gzip.compress(res_json.encode('utf-8'))

        return Response(content=compressed_data, media_type="application/json", headers={"Content-Encoding": "gzip"})
    except requests.exceptions.RequestException as e:

        print(f"Error posting to http://localhost:7000/placesInfo/place: {e}")
        raise HTTPException(
            status_code=500, detail="Failed to retrieve places information")
