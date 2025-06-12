from fastapi import FastAPI, HTTPException
import httpx
import os
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import List, Optional, Dict, Any

# Load environment variables
load_dotenv()

# Get API key from environment variables
OPENCAGE_API_KEY = os.getenv("OPENCAGE_API_KEY")

app = FastAPI(
    title="Indian Postal Code API",
    description="API for retrieving address details and geolocation for Indian postal codes",
    version="1.0.0"
)

class PostOffice(BaseModel):
    Name: str
    Description: Optional[str] = None
    BranchType: str
    DeliveryStatus: str
    Circle: str
    District: str
    Division: str
    Region: str
    Block: str
    State: str
    Country: str
    Pincode: str

class PincodeResponse(BaseModel):
    Message: str
    Status: str
    PostOffice: Optional[List[PostOffice]] = None

class GeoLocation(BaseModel):
    latitude: float
    longitude: float

class AddressDetails(BaseModel):
    pincode: str
    post_offices: List[PostOffice]
    geolocation: Optional[GeoLocation] = None

@app.get("/")
def read_root():
    return {"message": "Welcome to the Indian Postal Code API"}

@app.get("/api/pincode/{pincode}", response_model=AddressDetails)
async def get_address_details(pincode: str):
    """
    Get address details and geolocation for an Indian postal code
    
    - **pincode**: 6-digit Indian postal PIN code
    
    Returns address details and geolocation information
    """
    # Validate pincode (basic validation)
    if not pincode.isdigit() or len(pincode) != 6:
        raise HTTPException(status_code=400, detail="Invalid PIN code. Must be a 6-digit number.")
    
    # Create a client for making HTTP requests
    async with httpx.AsyncClient() as client:
        # Step 1: Get postal information from Postal PIN code API
        postal_response = await client.get(f"https://api.postalpincode.in/pincode/{pincode}")
        
        if postal_response.status_code != 200:
            raise HTTPException(status_code=502, detail="Failed to fetch data from Postal PIN code API")
        
        postal_data = postal_response.json()
        
        if not postal_data or postal_data[0]["Status"] != "Success":
            raise HTTPException(status_code=404, detail="PIN code not found or invalid")
        
        post_offices = postal_data[0]["PostOffice"]
        
        # Step 2: Get geolocation from OpenCage API
        # We use the state from the first post office for better geocoding
        state = post_offices[0]["State"]
        geocode_query = f"{pincode} {state} India"
        
        if not OPENCAGE_API_KEY:
            # Skip geocoding if API key is not available
            geolocation = None
        else:
            geocode_response = await client.get(
                "https://api.opencagedata.com/geocode/v1/json",
                params={
                    "q": geocode_query,
                    "key": OPENCAGE_API_KEY,
                    "limit": 1
                }
            )
            
            if geocode_response.status_code != 200:
                # Don't fail the whole request if geocoding fails
                geolocation = None
            else:
                geocode_data = geocode_response.json()
                
                if geocode_data["results"] and len(geocode_data["results"]) > 0:
                    coordinates = geocode_data["results"][0]["geometry"]
                    geolocation = GeoLocation(
                        latitude=coordinates["lat"],
                        longitude=coordinates["lng"]
                    )
                else:
                    geolocation = None
        
        # Return combined response
        return AddressDetails(
            pincode=pincode,
            post_offices=post_offices,
            geolocation=geolocation
        )
