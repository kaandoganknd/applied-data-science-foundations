# SPSS Data Quality and Descriptive Statistics

Week 2 practical work for an Applied Data Science module.

## Individual practical: Iris data quality

The Iris exercise checks missing values, duplicated records, and potential outliers before producing a cleaned dataset. The workflow removes three duplicated records, replaces six missing measurements with the median for the corresponding species, and retains IQR-flagged measurements after review rather than deleting plausible observations automatically.

## Collaborative practical: Weather statistics

The Weather exercise checks completeness, duplicate dates, and basic data validity before calculating descriptive statistics for precipitation, maximum temperature, minimum temperature, and wind speed. Potentially extreme precipitation and wind values are reviewed but retained because they can represent valid weather events.

## Files

- `syntax/iris_data_quality.sps` — import, audit, cleaning, outlier review, and export workflow for Iris.
- `syntax/weather_descriptive_statistics.sps` — import, cleaning checks, descriptive statistics, outlier review, and export workflow for Weather.
- `results-summary.md` — checked row counts, quality findings, and descriptive values.
- `data/README.md` — source-data and rerun instructions.

## Run in SPSS

Open a syntax file in IBM SPSS Statistics, update the two absolute file paths if necessary, select **Run All**, then save or export the generated output. The exact code is kept in the repository so each step remains inspectable.
