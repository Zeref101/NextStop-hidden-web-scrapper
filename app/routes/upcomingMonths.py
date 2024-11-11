from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import requests
from bs4 import BeautifulSoup

router = APIRouter()


class PlacesResponse(BaseModel):
    general_description: str
    places_data: list


@router.get("/places-by-month/{month}", response_model=PlacesResponse)
async def get_places_by_month(month: str):
    """
    Fetches the best places to visit in India for the given month.
    Returns the general description and a list of places with their details.
    """
    data = getPlacesByMonths(month)

    if "error" in data:
        raise HTTPException(status_code=500, detail=data["error"])

    return {
        "general_description": data["general_description"],
        "places_data": data["places_data"]
    }


def getPlacesByMonths(month: str):
    """
    Function to scrape data from the Holidify website based on the provided month.
    """
    # URL of the page to scrape
    url = f"https://www.holidify.com/collections/best-places-to-visit-in-{
        month}-in-india"

    try:
        # Send a GET request to the webpage
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception if there's an error with the request

        # Parse the page content with BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Function to scrape data
        def scrape_data(soup):
            # Extract general description
            general_description = soup.find(
                'div', class_='readMoreSmall font-smaller mb-3')
            if general_description:
                general_description = general_description.get_text(strip=True)
            else:
                general_description = "No general description found"

            # Extract each card content
            cards = soup.find_all('div', class_='card content-card')
            data = []
            for card in cards:
                # Extract title
                title = card.find('h3', class_='card-heading')
                title = title.get_text(
                    strip=True) if title else "No title found"

                # Extract image URL
                image = card.find('img', class_='card-img-top')
                image_url = (
                    image.get('data-original') if image and image.get('data-original')
                    else image.get('src') if image
                    else "No image found"
                )

                # Extract description
                description = card.find('p', class_='card-text')
                description = description.get_text(
                    strip=True) if description else "No description found"

                # Collect the extracted data
                card_data = {
                    'title': title,
                    'image_url': image_url,
                    'description': description
                }
                data.append(card_data)

            return general_description, data

        # Call the function to scrape data
        general_description, places_data = scrape_data(soup)

        return {
            "general_description": general_description,
            "places_data": places_data
        }

    except requests.exceptions.RequestException as e:
        # Handle any errors related to the HTTP request
        print(f"Error fetching data from {url}: {e}")
        return {
            "error": "Failed to retrieve data due to an HTTP request error"
        }
    except Exception as e:
        # Handle any other unexpected errors
        print(f"An unexpected error occurred: {e}")
        return {
            "error": "An unexpected error occurred while processing the data"
        }
