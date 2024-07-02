from bs4 import BeautifulSoup
import re
import requests


def find_places_in_country_name(location: str):

    if location:
        location = location.replace(" ", "-")
    url = f"https://www.holidify.com/country/{location}/places-to-visit.html"
    response = requests.get(url)

    if response.status_code == 404:
        return {"error": "Location not found"}

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

    return places_info
