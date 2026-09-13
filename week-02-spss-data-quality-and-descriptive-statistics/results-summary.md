# Results Summary

This note records the data checks behind the SPSS syntax. It is not a substitute for the SPSS Viewer output; the supplied `.sps` files reproduce the full audit and descriptive-statistics workflow.

## Iris data quality and cleaning

- **153 rows** and **6 variables** were received.
- **Three exact duplicate records** were identified. The cleaning syntax retains one copy of each duplicated record.
- **Six missing numeric measurements** were identified: three in `SepalWidthCm` and three in `PetalLengthCm`.
- Missing values are replaced using the **median measurement within the corresponding species**, avoiding a single overall-value substitution.
- IQR review identifies four potentially unusual sepal-width observations. They are retained because they are plausible botanical measurements and no source evidence indicates an entry error.
- The expected cleaned dataset contains **150 rows** with no missing numeric measurements.

## Weather data quality and descriptive statistics

- **1,461 daily observations** cover **2012-01-01 to 2015-12-31**.
- No missing values, duplicate dates, negative precipitation or wind readings, or `temp_max < temp_min` records were identified.
- The data therefore require no row removal. Precipitation and wind observations flagged by an IQR review are retained as valid candidate weather extremes.

| Measure | Mean | Standard deviation | Minimum | Maximum |
|---|---:|---:|---:|---:|
| Precipitation | 3.03 | 6.68 | 0.00 | 55.90 |
| Maximum temperature | 16.44 | 7.35 | -1.60 | 35.60 |
| Minimum temperature | 8.23 | 5.02 | -7.10 | 18.30 |
| Wind speed | 3.24 | 1.44 | 0.40 | 9.50 |

The Weather syntax produces the complete SPSS frequencies, descriptive measures, histograms and boxplots required for the exercise.
