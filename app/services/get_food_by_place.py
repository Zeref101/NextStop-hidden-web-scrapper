import gzip
import json
from bs4 import BeautifulSoup
import requests
from fastapi import APIRouter, HTTPException, Response

router = APIRouter()


def scrape_food_info(place_name: str):
    url = f"https://www.holidify.com/places/{
        place_name}/restaurants-places-to-eat-local-cuisine.html"
    try:
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        # Fetch general description
        general_description = ""
        heading_tag = soup.find("h2", class_="heading2 w-100")
        if heading_tag:
            read_more_div = heading_tag.find_next_sibling(
                "div", class_="readMoreText compact")
            if read_more_div:
                general_description = read_more_div.get_text(
                    separator=" ", strip=True)

        # Fetch each card with food details
        food_items = []
        for card in soup.find_all("div", class_="card content-card"):
            title = card.find("h3", class_="card-heading").get_text(
                strip=True) if card.find("h3", class_="card-heading") else "Unknown Title"

            # Image URL
            img_tag = card.find("img")
            img_url = img_tag.get("data-original") if img_tag and img_tag.get(
                "data-original") else img_tag.get("src") if img_tag else None

            # Description
            description = card.find("p", class_="card-text").get_text(
                strip=True) if card.find("p", class_="card-text") else "No description available"

            # Details Link
            details_link_tag = card.find("div", class_="content-card-footer").find(
                "a", class_="btn btn-read-more") if card.find("div", class_="content-card-footer") else None
            details_link = "https://www.holidify.com" + \
                details_link_tag["onclick"].split(
                    '"')[1] if details_link_tag else None

            # Append each food item to the list
            food_items.append({
                "title": title,
                "img_url": img_url,
                "description": description,
                "details_link": details_link
            })

        # Combine data into dictionary
        data = {
            "general_description": general_description,
            "food_items": food_items
        }

        return data

    except requests.RequestException as e:
        print(f"Error fetching data from {url}: {e}")
        return None


@router.get("/food/{place_name}")
async def get_food_info(place_name: str):
    data = scrape_food_info(place_name)
    if data is None:
        raise HTTPException(
            status_code=500, detail="Failed to retrieve food information")

    # Convert data to JSON and compress it
    json_data = json.dumps(data)
    compressed_data = gzip.compress(json_data.encode('utf-8'))

    return Response(content=compressed_data, media_type="application/json", headers={"Content-Encoding": "gzip"})
