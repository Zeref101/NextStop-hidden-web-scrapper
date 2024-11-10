from fastapi import APIRouter, HTTPException, Response
import gzip
import json
from app.services.get_food_by_place import scrape_food_info

router = APIRouter()


@router.get("/food/{place_name}")
async def get_food_info(place_name: str):
    try:
        # Call the scraping function
        print(place_name)
        food_info = scrape_food_info(place_name)

        # Check if food_info is empty
        if not food_info:
            raise HTTPException(
                status_code=404, detail="No food information found for this place.")

        # Convert the data to JSON
        res_json = json.dumps({"food_info": food_info})

        # Compress the data
        compressed_data = gzip.compress(res_json.encode('utf-8'))

        # Return the gzipped response
        return Response(content=compressed_data, media_type="application/json", headers={"Content-Encoding": "gzip"})

    except Exception as e:
        print(f"Error scraping food info: {e}")
        raise HTTPException(
            status_code=500, detail="Failed to retrieve food information.")
