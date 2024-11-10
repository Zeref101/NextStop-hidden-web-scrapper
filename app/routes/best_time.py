import gzip
import json
from bs4 import BeautifulSoup
import requests
from fastapi import APIRouter, HTTPException, Response

router = APIRouter()


def scrape_best_time_to_visit(place_name: str):
    url = f"https://www.holidify.com/places/{
        place_name}/best-time-to-visit.html"
    try:
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        # Locate the "What is the best time to visit <Place>?" section
        best_time_to_visit = ""
        best_time_section = soup.find("div", class_="row no-gutters mb-50")
        if best_time_section:
            heading = best_time_section.find("h2", class_="heading2 w-100")
            if heading:
                description_paragraph = heading.find_next_sibling("p")
                if description_paragraph:
                    best_time_to_visit = description_paragraph.get_text(
                        strip=True)

        # Locate the "Monthly Weather" table if it exists
        monthly_weather = []
        table_div = soup.find("div", class_="table-responsive")
        if table_div:
            table = table_div.find("table")
            if table:
                rows = table.find("tbody").find_all("tr")
                for row in rows:
                    columns = row.find_all("td")
                    if len(columns) >= 3:
                        month = columns[0].get_text(strip=True)
                        high_low_temp = columns[1].get_text(strip=True)
                        rain_days = columns[2].get_text(strip=True)
                        high, low = [temp.strip("°").strip()
                                     for temp in high_low_temp.split('/')]

                        monthly_weather.append({
                            "month": month,
                            "high": high,
                            "low": low
                        })

        # Combine data into a dictionary
        data = {
            "best_time_to_visit": best_time_to_visit,
            "monthly_weather": monthly_weather
        }

        return data

    except requests.RequestException as e:
        print(f"Error fetching data from {url}: {e}")
        return None


@router.get("/best-time-to-visit/{place_name}")
async def get_best_time_to_visit(place_name: str):
    data = scrape_best_time_to_visit(place_name)
    if data is None:
        raise HTTPException(
            status_code=500, detail="Failed to retrieve best time to visit information")

    # Convert data to JSON and compress it
    json_data = json.dumps(data)
    compressed_data = gzip.compress(json_data.encode('utf-8'))

    return Response(content=compressed_data, media_type="application/json", headers={"Content-Encoding": "gzip"})
