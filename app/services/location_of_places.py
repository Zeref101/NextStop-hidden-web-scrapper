from geopy.geocoders import Nominatim
import re


def get_location_type(location: str):
    geolocator = Nominatim(user_agent="NextStop")
    location = geolocator.geocode(
        location, exactly_one=True, addressdetails=True)

    if location:
        address = location.raw.get('address', {})

        # print(address)

        state = address.get("state", "").lower()
        country = address.get("country", "").lower()
        city_or_rural = address.get("city") or address. get(
            "town") or address.get("village") or address.get("county")

        if city_or_rural:
            city_or_rural = re.sub(r"\s*\([^)]*\)", "", city_or_rural)
            city_or_rural = city_or_rural.lower()

        if country and not state and not city_or_rural:
            return {"country": country}

        elif state and not city_or_rural:
            return {"state": state, "country": country} if country else {"state": state}

        elif city_or_rural:
            location_details = {"country": country} if country else {}
            if state:
                location_details["state"] = state
            location_details["city_rural_urban_county"] = city_or_rural
            return location_details

    return {"error": "Location not found"}
