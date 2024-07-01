from bs4 import BeautifulSoup
import requests
from fastapi import APIRouter
import re

router = APIRouter()


@router.get("/places/{location}")
async def get_places_to_visit(location: str):
    url = f"https://www.holidify.com/places/{location}/sightseeing-and-things-to-do.html"

    response = requests.get(url)

    soup = BeautifulSoup(response.content, 'html.parser')

    places_divs = soup.find_all('div', 'col-12 col-md-6 pr-md-3')

    places_info = []

    for div in places_divs:
        title = div.find('h3', class_='card-heading').text.strip()
        title = re.sub(r'^\d+\.\s*', '', title)

        img_url = div.find('img', class_='card-img-top')['data-original']

        description = div.find('p', class_='card-text').text.strip()

        places_dict = {
            'title': title,
            'img_url': img_url,
            'description': description
        }

        places_info.append(places_dict)

    return places_info