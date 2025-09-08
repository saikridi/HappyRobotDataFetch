from fastapi import FastAPI
import pandas as pd
import uvicorn
import sys
import os

# Add the src directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from DataFetchFiles import get_endpoints

app = FastAPI(title="Carrier Data API")

# Load CSV data
df = pd.read_csv("HappyRobot/src/Resources/inbound_carrier_data.csv")

@app.post("/")
async def root():
    return {"message": "Carrier Data API", "version": "1.0.0"}


@app.post("/getLoads")
async def get_carrier_endpoint(request: get_endpoints.LoadRequest):
    """Get specific carrier by load_id from JSON request"""
    return await get_endpoints.get_carrier(request, df)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
