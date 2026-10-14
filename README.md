# Napa County Traffic Collision Data Analysis

A SQL analysis of California Crash Reporting System (CCRS) data for Napa County, using PostgreSQL in a Jupyter notebook.

**[View the dashboard →](https://cillam.com/projects/napa_crashes/)**

## The Questions

This project asks:

1. What time of day and day of week are crashes most common?
2. How have crashes changed year over year?
3. How often is an impairment such as alcohol involved, and does it peak at certain times or on weekends?

## Key Findings

The analysis covers **17,886 crashes in Napa County from January 2016 to early October 2026**.

- **Crash volume follows the daily traffic cycle.** About a third of crashes (5,949) happen between noon and 5 p.m., with the heaviest concentration on weekday afternoons. The 1–5 a.m. window is the quietest, with 1,034 crashes.
- **Crashes dropped in 2020 and have only slightly picked back up.** Every year since 2021 has come in below the 2016–2019 range.
- **About 1 in 8 crashes (13.1%) involved someone under the influence**, and 16.1% involved someone who had been drinking. Drug-only cases are under 1%.
- **Impairment is a late-night problem.** Under 5% of daytime weekday crashes involve someone under the influence. After 9 p.m., that share rises to about 31%, and on weekends between 1 and 5 a.m. it reaches 44.8%.
- **Wine-tasting hours are not the main risk window.** Weekend afternoons have an impairment share of 9.2%, about double the weekday afternoon rate but below the countywide average.

Because the data has no traffic counts, these are crash counts and shares, not risk rates. See [Limitations](#limitations).

## Data

- **Source:** [California Crash Reporting System (CCRS), via the California Open Data Portal](https://data.ca.gov/@california-highway-patrol/ccrs)
- **Coverage:** Napa County, 2016–Present
- Raw CSVs are **not** included in this repo. Download them from the source above and place them in `data/`. Download script provided.


## Repo Structure

```
├── README.md
├── download_ccrs.py            # download CCRS CSVs
├── napa_crash_analysis.ipynb   # data validation and EDA
├── requirements.txt
├── data/                       # directory for raw CSVs (git-ignored)
└── visualizations/             # exported charts/images
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
- **Coded, ambiguous, and missing values** required cleanup decisions, which are documented in the notebook.
- These findings show **associations, not causes**.

## Next Steps

### More questions for this data
- **Who is involved, and who gets hurt?** Compare at-fault rates by driver age group, and injury rates for drivers, passengers, pedestrians, and cyclists.
- **Are older vehicles less safe?** When a crash happens, are people in older vehicles more likely to be seriously hurt? Does seat position or ejection make a difference?
- **What makes a crash severe?** Compare serious-injury rates by lighting, weather, road surface, and crash type.
- **Is there a seasonal pattern?** Check whether harvest season (August–October) stands out from the rest of the year.
- **Where exactly do crashes cluster?** Map crash locations to find hot spots.
- **Has impaired driving changed over time?** Track the share of crashes involving someone under the influence by year, overall, at night, and on weekend afternoons, to see whether patterns shifted with events like the 2020 traffic drop or the growth of ride-sharing, and whether weekend tasting-hour crashes are rising or falling.
- - **Is there a seasonal pattern?** Check which months have the most crashes, and whether the holidays or harvest season (August–October) stand out.
- **Which roads have the most crashes?** Rank roads by crash count, both countywide and within each city, and compare Highway 29 with the Silverado Trail. This first requires standardizing road names: the raw data has over 2,200 spellings (for example, "SR-29," "HWY 29," and "St. Helena Hwy" are all Highway 29), plus ramp descriptions and house numbers. Local roads also need to be identified by city as well as name, since different roads can share a name, while highways should be treated as one road countywide.


### Future Work

#### 1. Evaluate pedestrian safety improvements
Estimate how much each pedestrian safety treatment (high-visibility crosswalks, RRFBs, bulb-outs, median refuges, crossing barriers) changed crashes at its location.
- **Site inventory:** compile a table of treated sites with treatment type, install dates, and cost, using County and city records, grant filings, and the Napa County and City of Napa Local Roadway Safety Plans.
- **Spatial matching:** add PostGIS to assign crashes to treated sites by distance, with sensitivity tests at several buffer sizes.
- **Questions:** Did pedestrian crashes and killed-or-seriously-injured (KSI) crashes fall at treated sites beyond the countywide trend? Which treatments delivered the most reduction per dollar?

#### 2. Build a public crash dashboard
A resident-facing web dashboard to explore Napa County crashes by year, place, and type.
- **Live data:** read CCRS directly from the data.ca.gov API through a small caching layer, so new crashes appear without re-running anything.
- **Views:** yearly trends, a crash map, KSI hot spots, crash factors, and before-after results for each treated site.
- **Draw-an-area search:** residents draw a boundary on the map, or pick a preset area such as a city or school zone, and every chart updates to show only crashes inside it.
- **Privacy and accessibility:** age and sex shown only in aggregate, never on individual crashes; plain-language labels; WCAG-compliant and mobile-friendly.

### Data improvements
- Geocode crashes with missing coordinates so every crash can be mapped (Some have locations provided but not coordinates.).
- Add traffic and pedestrian volume data (Caltrans AADT, local counts) to move from crash counts to crash rates.

