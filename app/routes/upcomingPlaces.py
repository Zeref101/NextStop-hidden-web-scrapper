from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import requests
from bs4 import BeautifulSoup
from typing import List

router = APIRouter()


class UpcomingPlace(BaseModel):
    img_url: str
    month: str


class UpcomingPlacesResponse(BaseModel):
    places_data: List[UpcomingPlace]


@router.get("/upcoming-places", response_model=UpcomingPlacesResponse)
async def get_upcoming_places():
    """
    Fetches upcoming places with their images and months.
    """
    data = scrape_upcoming_places()

    if "error" in data:
        raise HTTPException(status_code=500, detail=data["error"])

    return {
        "places_data": data["places_data"]
    }


def scrape_upcoming_places():

    url = "https://www.holidify.com/"  # Replace with the actual URL

    try:
        # Send a GET request to the webpage
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses

        # Parse the page content with BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        print(soup)
        # Locate the <h2> tag with the class 'heading2 w-100' and the specific text
        heading = soup.find('h2', class_='heading2 w-100',
                            string="Countries to visit in upcoming months")
        print(heading)
        if not heading:
            return {"error": "Heading for upcoming places not found"}

        # Find the container after the <h2> tag, assuming it holds the upcoming places data
        upcoming_places_container = heading.find_next(
            'div', class_='slick-slide slick-current slick-active')
        if not upcoming_places_container:
            return {"error": "Upcoming places container not found"}

        # Collect data within the container
        places_data = []
        slides = upcoming_places_container.find_all(
            'div', class_='slick-slide')

        for slide in slides:
            # Extract image URL from data attribute
            image_div = slide.select_one('.lazyBG')
            img_url = image_div.get(
                'data-original') if image_div else "No image URL found"

            # Extract month title text
            month_title = slide.select_one('.main-title')
            month = month_title.text.strip() if month_title else "No month found"

            if img_url and month:
                places_data.append({
                    'img_url': img_url,
                    'month': month
                })

        return {"places_data": places_data}

    except requests.exceptions.RequestException as e:
        # Handle HTTP request errors
        print(f"Error fetching data from {url}: {e}")
        return {"error": "Failed to retrieve data due to an HTTP request error"}

    except Exception as e:
        # Handle other unexpected errors
        print(f"An unexpected error occurred: {e}")
        return {"error": "An unexpected error occurred while processing the data"}
