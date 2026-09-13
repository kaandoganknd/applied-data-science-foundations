# Source Data

This directory intentionally excludes the supplied source files:

- `Salary_data.xlsx`
- `House_prices.csv`
- `weather.xlsx`

Place the original files in this directory, or edit the `GET DATA` path at the beginning of each `.sps` file. The analyses use the following sheets where applicable:

- `Salary_data.xlsx`: `in`
- `weather.xlsx`: `weather`

No cleaned dataset is exported. The syntax retains potentially valid outliers and shows the diagnostics required to make any later cleaning decision transparent.
