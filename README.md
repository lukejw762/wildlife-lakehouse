# Wildlife Lakehouse

A end-to-end data engineering portfolio project that ingests elk occurrence data from a public REST API, loads it into a cloud data warehouse, and transforms it into curated analytical models — demonstrating modern lakehouse patterns including pipeline orchestration, data modeling, and data quality frameworks.

---

## Motivation

This project was built to demonstrate practical data engineering skills in a real-world context. Elk population data is directly relevant to wildlife conservation organizations and outdoor technology companies focused on public land mapping and habitat tracking. The dataset is sourced from the [Global Biodiversity Information Facility (GBIF)](https://www.gbif.org/), a free public API with over 31,000 elk sighting records across the United States.

---

## Architecture

```
GBIF REST API
     │
     ▼
Python Ingestion Script
(pagination, field extraction, flattening)
     │
     ▼
BigQuery — wildlife_raw.elk_sightings_raw
(raw landing table)
     │
     ▼
dbt Transformation Models
(cleaning, KPI definitions, curated datasets)
     │
     ▼
Tableau Public Dashboard
(sighting trends, geographic distribution)

Orchestrated end-to-end by Apache Airflow (Docker)
```

---

## Tech Stack

| Layer | Tool |
|---|---|
| Orchestration | Apache Airflow (Docker) |
| Ingestion | Python, Requests |
| Data Warehouse | Google BigQuery |
| Transformation | dbt Core |
| Dashboard | Tableau Public |
| Version Control | Git / GitHub |
| Development | VS Code, Jupyter Notebooks |

---

## Project Structure

```
wildlife-lakehouse/
├── dags/                   # Airflow DAG definitions
├── scripts/                # Python ingestion scripts
├── wildlife_lakehouse/     # dbt models and transformations
├── config/                 # GCP credentials (gitignored)
├── docker-compose.yaml     # Airflow local environment
├── Dockerfile              
├── requirements.txt        
└── .env                    # Environment variables (gitignored)
```

---

## Setup

### Prerequisites
- Docker Desktop
- Python 3.x with pip
- Google Cloud account with BigQuery enabled
- A GCP service account key with BigQuery Admin permissions

### Running Locally

1. **Clone the repo**
   ```bash
   git clone https://github.com/lukejw762/wildlife-lakehouse.git
   cd wildlife-lakehouse
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   venv\Scripts\activate        # Windows
   pip install -r requirements.txt
   ```

3. **Add GCP credentials**
   - Place your service account JSON key in the `config/` folder
   - Update `.env` with your credentials path:
     ```
     AIRFLOW_UID=50000
     GOOGLE_APPLICATION_CREDENTIALS=/opt/airflow/config/your-key.json
     ```

4. **Start Airflow**
   ```bash
   docker compose up airflow-init
   docker compose up -d
   ```
   Access the Airflow UI at `http://localhost:8080` (user: `airflow`, password: `airflow`)

5. **Run the ingestion script**
   Open `scripts/ingest_elk_occurrences.ipynb` in VS Code and run all cells. This will pull the 2,000 most recent elk sighting records from the GBIF API and load them into BigQuery.

---

## Roadmap

- [ ] Convert ingestion notebook to a production Python script
- [ ] Wire ingestion into an Airflow DAG on a weekly schedule
- [ ] Add data quality checks and automated validation
- [ ] Build Tableau Public dashboard with sighting trends and geographic distribution
- [ ] Add metadata and lineage documentation
- [ ] Expand dataset to include additional ungulate species

---

## Data Source

[GBIF Occurrence API](https://www.gbif.org/developer/occurrence) — Global Biodiversity Information Facility. Free and open access to biodiversity data.
