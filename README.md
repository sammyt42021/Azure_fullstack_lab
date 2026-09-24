# Azure_fullstack_lab

# eClipseBord

eClipseBord is a full-stack dashboard for exploring NASA solar eclipse data. FastAPI reads and filters the dataset, while Streamlit displays the results.

## Architecture

```text
Browser
  ↓
Streamlit frontend
  ↓ HTTP request
FastAPI backend
  ↓
NASA solar eclipse CSV dataset
```

Local Docker uses `http://backend:8000` because `backend` is Docker Compose’s internal service name. In Azure, the frontend uses the public HTTPS address of the deployed FastAPI backend.

## Project structure

```text
backend/
  data/solar.csv                 # NASA dataset
  src/backend/api.py             # FastAPI endpoints
  src/backend/data_processing.py # Reads and prepares CSV data
  src/backend/constants.py       # Dataset path

frontend/
  src/frontend/dashboard.py      # Streamlit dashboard

eda/explore.py                   # Short EDA
dockerfiles/                     # Dockerfiles
docker-compose.yaml              # Starts backend and frontend
```

## Dataset and EDA

Dataset: [NASA Solar Eclipses on Kaggle](https://www.kaggle.com/datasets/nasa/solar-eclipses)

The dataset contains 11,898 eclipse records and 15 columns. The EDA identifies four eclipse types:

- `P`: Partial
- `A`: Annular
- `T`: Total
- `H`: Hybrid

Run the EDA:

```bash
uv run python eda/explore.py
```

## Run locally

Install dependencies:

```bash
uv sync --all-packages
```

Start the FastAPI backend:

```bash
uv run uvicorn backend.api:app --reload --port 8000
```

Start the Streamlit frontend in a second terminal:

```bash
uv run streamlit run frontend/src/frontend/dashboard.py
```

Open:

- Dashboard: `http://localhost:8501`
- API health check: `http://localhost:8000/health`
- API documentation: `http://localhost:8000/docs`

## Run with Docker

Build and start both services:

```bash
docker compose up --build
```

Open the dashboard at `http://localhost:8501`.

Stop the containers:

```bash
docker compose down
```

## Deployment

The application is deployed on Azure:

- Frontend: <https://eclipsebord-ui-tobi2026.azurewebsites.net>
- Backend API: <https://eclipsebord-api.wonderfulplant-33aebbbf.norwayeast.azurecontainerapps.io>

Azure flow:

```text
Azure Container Registry
  ├── eclipsebord-backend:v1 → Azure Container App
  └── eclipsebord-frontend:v1 → Azure App Service
```

The App Service frontend receives the backend address through its `BACKEND_URL` environment variable.

## Cleanup

After the recorded demonstration and submission, delete the Azure resource group to stop charges:

```bash
az group delete --name eclipsebord-rg --yes --no-wait
```