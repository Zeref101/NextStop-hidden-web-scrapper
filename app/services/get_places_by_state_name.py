from bs4 import BeautifulSoup
import re
import requests
import json


def find_places_in_state_name(location: str):

    if location:
        location = location.replace(" ", "-")
    url = f"https://www.holidify.com/state/{location}/top-destinations-places-to-visit.html"
    response = requests.get(url)

    if response.status_code == 404:
        url2 = f"https://www.holidify.com/places/{location}/sightseeing-and-things-to-do.html"
        response = requests.get(url2)

    if response.status_code == 404:
        return json.dumps({"error": "Location not found"})

    soup = BeautifulSoup(response.content, 'html.parser')

    places_divs = soup.find_all('div', 'col-12 col-md-6 pr-md-3')

    # print(places_divs)
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

    json_string = json.dumps(places_info, ensure_ascii=False)

    return json_string
