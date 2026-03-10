# Wildlife Lakehouse

An end-to-end data engineering portfolio project that ingests elk occurrence data from a public REST API, loads it into a cloud data warehouse, and transforms it into curated analytical models — demonstrating modern lakehouse patterns including ELT pipeline orchestration, dimensional modeling, and automated data quality frameworks.

## Motivation

This project was built to demonstrate practical data engineering skills in a real-world context. The dataset is sourced from the **Global Biodiversity Information Facility (GBIF)**, a free public API with over 31,000 elk sighting records across the United States.

## Architecture

```
GBIF REST API
     │
     ▼
Python Ingestion Script
(pagination, field extraction, flattening)
     │
     ▼
BigQuery — wildlife_raw.elk_sighting_raw
(bronze / raw landing table)
     │
     ▼
dbt Staging Layer — wildlife_staging
(cleaning, renaming, null filtering)
     │
     ▼
dbt Intermediate Layer — wildlife_intermediate
(business logic, derived fields, validation flags)
     │
     ▼
dbt Marts Layer — wildlife_marts
(star schema: facts, dimensions, aggregations)
     │
     ▼
Tableau Public Dashboard (in progress)
(sighting trends, geographic distribution)

Orchestrated end-to-end by Apache Airflow (Docker)
CI/CD via GitHub Actions on every push to main
```

## Medallion Architecture

This project implements the **Medallion Architecture** (Bronze / Silver / Gold) pattern:

| Layer | Dataset | Description |
|---|---|---|
| Bronze | `wildlife_raw` | Raw API data, loaded as-is |
| Silver | `wildlife_staging` / `wildlife_intermediate` | Cleaned, standardized, enriched |
| Gold | `wildlife_marts` | Star schema facts, dimensions, and aggregations |

## Tech Stack

| Layer | Tool |
|---|---|
| Orchestration | Apache Airflow (Docker) |
| Ingestion | Python, Requests |
| Data Warehouse | Google BigQuery |
| Transformation | dbt Core |
| Data Quality | dbt Tests (generic + singular) |
| CI/CD | GitHub Actions |
| Dashboard | Tableau Public |
| Version Control | Git / GitHub |
| Development | VS Code, Jupyter Notebooks |

## Project Structure

```
wildlife-lakehouse/
├── .github/
│   └── workflows/
│       └── dbt_ci.yml              # GitHub Actions CI/CD workflow
├── dags/                           # Airflow DAG definitions
├── scripts/                        # Python ingestion scripts
│   └── ingest_elk_occurrences.py   # GBIF API ingestion
├── wildlife_lakehouse/             # dbt project
│   ├── models/
│   │   ├── staging/                # Bronze → Silver cleaning layer
│   │   │   ├── stg_elk_sightings.sql
│   │   │   ├── stg_elk_sightings.yml
│   │   │   └── sources.yml
│   │   ├── intermediate/           # Business logic and derived fields
│   │   │   ├── int_elk_sightings.sql
│   │   │   └── int_elk_sightings.yml
│   │   └── marts/                  # Gold layer — star schema
│   │       ├── dimensions/
│   │       │   ├── dim_date.sql
│   │       │   ├── dim_location.sql
│   │       ├── facts/
│   │       │   └── fct_elk_sightings.sql
│   │       └── aggregations/
│   │           └── mart_elk_sightings_state_agg.sql
│   ├── macros/
│   │   └── generate_schema_name.sql
│   ├── tests/
│   │   └── assert_valid_coordinates.sql
│   └── dbt_project.yml
├── profiles.yml                    # dbt connection profile (CI use)
├── config/                         # GCP credentials (gitignored)
├── docker-compose.yaml             # Airflow local environment
├── Dockerfile
├── requirements.txt
└── .env                            # Environment variables (gitignored)
```

## Data Quality

This project implements a two-layer data quality framework:

**dbt Generic Tests** (defined in model YAML files)
- Uniqueness and not-null checks on primary keys
- Accepted values validation on categorical fields (season, coordinate quality)

**dbt Singular Tests** (custom SQL in `tests/`)
- Coordinate range validation — latitude between -90/90, longitude between -180/180

**CI/CD Pipeline** (GitHub Actions)
- On every push to `main`, GitHub automatically spins up a clean environment, runs `dbt run` and `dbt test`, and reports pass/fail — blocking merges if tests fail.

## dbt Model Lineage

```
elk_sighting_raw (BigQuery source)
        │
        ▼
stg_elk_sightings       ← renamed columns, null filtering, date construction
        │
        ▼
int_elk_sightings       ← season derivation, coordinate quality tiers, validation flags
        │
        ├──▶ dim_date
        ├──▶ dim_location
        ├──▶ fct_elk_sightings
        └──▶ mart_elk_sightings_state_agg
```

## Setup

### Prerequisites
- Docker Desktop
- Python 3.11
- Google Cloud account with BigQuery enabled
- A GCP service account key with BigQuery Admin permissions

### Running Locally

1. Clone the repo
```bash
git clone https://github.com/lukejw762/wildlife-lakehouse.git
cd wildlife-lakehouse
```

2. Create a virtual environment
```bash
py -3.11 -m venv venv311
venv311\Scripts\activate        # Windows
pip install -r requirements.txt
```

3. Add GCP credentials
   - Place your service account JSON key in the `config/` folder
   - Update `.env` with your credentials path:
```
AIRFLOW_UID=50000
GOOGLE_APPLICATION_CREDENTIALS=/opt/airflow/config/your-key.json
```

4. Start Airflow
```bash
docker compose up airflow-init
docker compose up -d
```
Access the Airflow UI at `http://localhost:8080` (user: `airflow`, password: `airflow`)

5. Run the ingestion script
```bash
python scripts/ingest_elk_occurrences.py
```
This pulls the 2,000 most recent elk sighting records from the GBIF API and loads them into BigQuery.

6. Run dbt transformations
```bash
dbt run --project-dir wildlife_lakehouse
dbt test --project-dir wildlife_lakehouse
```

## Roadmap
- [ ] Wire ingestion and dbt into a full Airflow DAG on a weekly schedule (in progress)
- [ ] Build Tableau Public dashboard with sighting trends and geographic distribution (in progress)
- [ ] Add metadata and lineage documentation
- [ ] Expand dataset to include additional species (mule deer, pronghorn)
- [ ] Ingest NOAA weather data by coordinates to enrich sighting records with temperature and precipitation context. To enable multi-source joins and more complex analytical models
- [ ] Expand CI/CD pipeline to include environment promotion (dev → prod)

## Data Source

**GBIF Occurrence API** — Global Biodiversity Information Facility. Free and open access to biodiversity data. [https://www.gbif.org](https://www.gbif.org)
