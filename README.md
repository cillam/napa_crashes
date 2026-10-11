# Napa County Traffic Collision Data Analysis

A SQL analysis of California Crash Reporting System (CCRS) data for Napa County, using PostgreSQL in a Jupyter notebook.


## The Question

Napa County hosts millions of wine-country visitors a year, many of them driving between tasting rooms on two-lane roads like Highway 29 and the Silverado Trail. This project asks:

**When, where, and under what conditions do crashes happen in Napa County, and how much does alcohol play a role?**

1. What time of day and day of week are crashes most common?
2. Is there a seasonal pattern, and does harvest season stand out? How have crashes trended year over year?
3. How often is alcohol involved, and when?
4. Who is involved in crashes, and who gets hurt?
5. Which cities and roads have the most crashes?
6. Which conditions make a crash more likely to be severe?

## Key Findings

TBD

## Data

- **Source:** [California Crash Reporting System (CCRS), via the California Open Data Portal](https://data.ca.gov/@california-highway-patrol/ccrs)
- **Coverage:** Napa County, 2016–Present
- Raw CSVs are **not** included in this repo. Download them from the source above and place them in `data/`. Download script provided.

## SQL Techniques Demonstrated

TBD

## Repo Structure

```
├── README.md
├── download_ccrs.py            # download CCRS CSVs
├── napa_crash_analysis.ipynb   # data validation and EDA
├── requirements.txt
├── data/                       # directory for raw CSVs (git-ignored)
└── visualizations/             # exported charts
```

## How to Run

1. **Start PostgreSQL** (Postgres.app, Homebrew, Docker container, whatever)
2. **Download the CCRS CSVs** into `data/`. Download script provided. 
3. **Install requirements** listed in `requirements.txt`.
4. **Set database URL** as an environment variable. Example .env provided.
5. **Open the notebook** and run it top to bottom.

## Limitations

- **Counts are not risk.** Without traffic-volume data, a busy road will show more crashes even if it is no more dangerous per mile driven.
- **Reporting** varies across agencies and years.
- **Coded and missing values** required cleanup decisions, which are documented in the notebook.
- These findings show **associations, not causes**.

## Next Steps

This notebook is the first stage of a larger Napa County traffic safety project. The cleaned crash tables built here are the foundation for two follow-on pieces of work.

### 1. Evaluate pedestrian safety improvements
Estimate how much each pedestrian safety treatment (high-visibility crosswalks, RRFBs, bulb-outs, median refuges, crossing barriers) changed crashes at its location.
- **Site inventory:** compile a table of treated sites with treatment type, install dates, and cost, using County and city records, grant filings, and the Napa County and City of Napa Local Roadway Safety Plans.
- **Spatial matching:** add PostGIS to assign crashes to treated sites by distance, with sensitivity tests at several buffer sizes.
- **Questions:** Did pedestrian crashes and killed-or-seriously-injured (KSI) crashes fall at treated sites beyond the countywide trend? Which treatments delivered the most reduction per dollar?

### 2. Build a public crash dashboard
A resident-facing web dashboard to explore Napa County crashes by year, place, and type.
- **Live data:** read CCRS directly from the data.ca.gov API through a small caching layer, so new crashes appear without re-running anything.
- **Views:** yearly trends, a crash map, KSI hot spots, crash factors, and before-after results for each treated site.
- **Draw-an-area search:** residents draw a boundary on the map, or pick a preset area such as a city or school zone, and every chart updates to show only crashes inside it.
- **Privacy and accessibility:** age and sex shown only in aggregate, never on individual crashes; plain-language labels; WCAG-compliant and mobile-friendly.

### Data improvements
- Geocode crashes with missing coordinates so every crash can be mapped (Some have locations provided but not coordinates.).
- Add traffic and pedestrian volume data (Caltrans AADT, local counts) to move from crash counts to crash rates.

