# Carrier Data API

Simple FastAPI application to read and update carrier data from CSV file.

## Endpoints

- `GET /` - API information
- `GET /carriers` - Get all carrier data

## Local Development

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
cd src
python main.py
```

3. Access the API at: http://localhost:8080

## Google Cloud Deployment

### Option 1: App Engine
```bash
gcloud app deploy app.yaml
```

### Option 2: Cloud Run (with Docker)
```bash
# Build and push to Google Container Registry
gcloud builds submit --tag gcr.io/PROJECT_ID/carrier-api

# Deploy to Cloud Run
gcloud run deploy carrier-api --image gcr.io/PROJECT_ID/carrier-api --platform managed --region us-central1 --allow-unauthenticated
```

Replace `PROJECT_ID` with your Google Cloud project ID.

## API Usage Examples

### Get all carriers
```bash
curl http://localhost:8080/carriers
```

### Get specific carrier
```bash
curl http://localhost:8080/carriers/1
```

### Update carrier
```bash
curl -X PUT http://localhost:8080/carriers/1 \
  -H "Content-Type: application/json" \
  -d '{"notes": "Updated notes", "loadboard_rate": 5000.00}'
```
