# Indian Postal Code API

A RESTful API built with FastAPI that provides address details and geolocation information for Indian postal codes (PIN codes).

## Features

- Retrieve detailed information about locations associated with Indian PIN codes
- Get geolocation data (latitude and longitude) for PIN codes
- Fast and efficient API built with FastAPI

## Prerequisites

- Python 3.7+
- FastAPI
- httpx
- An OpenCage API key (for geolocation)

## Installation

1. Clone this repository:
   ```
   git clone <repository-url>
   cd python-location-api
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up your environment variables:
   - Create a `.env` file in the project root
   - Add your OpenCage API key:
     ```
     OPENCAGE_API_KEY=your_opencage_api_key_here
     ```
   - You can get a free API key from [OpenCage](https://opencagedata.com/)

## Running the API

Run the application with:

```
python run.py
```

The API will be available at `http://localhost:8000`.

## API Endpoints

### GET /api/pincode/{pincode}

Retrieves address details and geolocation for a given Indian postal code.

To access the endpoint
- **Open your browser** and go to `http://localhost:8000/api/pincode/{your_pincode}`
- **Test using Postman** by selecting `GET` as the method, send a request to `http://localhost:8000/api/pincode/{your_pincode}` 

**Parameters**:
- `pincode`: 6-digit Indian postal PIN code

**Example Request**:
```
GET /api/pincode/110001
```

**Example Response**:
```json
{
  "pincode": "110001",
  "post_offices": [
    {
      "Name": "Bengali Market",
      "BranchType": "Sub Post Office",
      "DeliveryStatus": "Delivery",
      "Circle": "Delhi",
      "District": "Central Delhi",
      "Division": "New Delhi Central",
      "Region": "Delhi",
      "Block": "New Delhi",
      "State": "Delhi",
      "Country": "India",
      "Pincode": "110001"
    },
    ...
  ],
  "geolocation": {
    "latitude": 28.6315,
    "longitude": 77.2167
  }
}
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.
