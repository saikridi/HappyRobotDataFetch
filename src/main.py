from fastapi import FastAPI
import pandas as pd
import uvicorn
from DataFetchFiles.get_endpoints import LoadRequest, get_carrier

app = FastAPI(title="Carrier Data API")

# Load CSV data
df = pd.read_csv("src/Resources/inbound_carrier_data.csv")

@app.get("/")
async def root():
    return {"message": "Carrier Data API", "version": "1.0.0"}


@app.get("/getLoads")
async def get_carrier_endpoint(request: LoadRequest):
    """Get specific carrier by load_id from JSON request"""
    return await get_carrier(request, df)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
