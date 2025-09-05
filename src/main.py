from fastapi import FastAPI
import pandas as pd
import uvicorn
from DataFetchFiles.get_endpoints import get_carrier, LoadIdRequest

app = FastAPI(title="Carrier Data API")

# Load CSV data
df = pd.read_csv("Resources/inbound_carrier_data.csv")

@app.get("/")
async def root():
    return {"message": "Carrier Data API", "version": "1.0.0"}


@app.get("/getLoads")
async def get_carrier_endpoint(request: LoadIdRequest):
    """Get specific carrier by load_id from JSON request"""
    return get_carrier(request, df)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
