* Week 2 collaborative practical: Weather descriptive statistics and data checks.
* Update the two file paths before running this syntax on another computer.

GET DATA
 /TYPE=XLSX
 /FILE='/Users/benjipro/Downloads/weather.xlsx'
 /SHEET=name 'weather'
 /READNAMES=ON.
EXECUTE.

DATASET NAME WeatherRaw.
FORMATS date (ADATE10) precipitation temp_max temp_min wind (F8.2).
VARIABLE LABELS
 date 'Observation date'
 precipitation 'Daily precipitation'
 temp_max 'Daily maximum temperature'
 temp_min 'Daily minimum temperature'
 wind 'Daily wind speed'
 weather 'Weather category'.

* Data completeness, duplicate-date check, and validity check.
FREQUENCIES VARIABLES=date precipitation temp_max temp_min wind weather
 /FORMAT=NOTABLE
 /ORDER=ANALYSIS.
SORT CASES BY date(A).
AGGREGATE
 /OUTFILE=* MODE=ADDVARIABLES
 /BREAK=date
 /date_count=N.
COMPUTE duplicate_date=(date_count>1).
COMPUTE invalid_numeric=(precipitation<0 OR wind<0 OR temp_max<temp_min).
FREQUENCIES VARIABLES=date_count duplicate_date invalid_numeric
 /FORMAT=NOTABLE
 /ORDER=ANALYSIS.

* Full descriptive statistics for the numeric weather measures.
FREQUENCIES VARIABLES=precipitation temp_max temp_min wind
 /STATISTICS=MEAN MEDIAN MODE STDDEV VARIANCE RANGE MINIMUM MAXIMUM SEMEAN SKEWNESS SESKEW KURTOSIS SEKURT
 /HISTOGRAM NORMAL
 /ORDER=ANALYSIS.
FREQUENCIES VARIABLES=weather
 /ORDER=ANALYSIS.

* Boxplots and extreme values support outlier review.
EXAMINE VARIABLES=precipitation temp_max temp_min wind
 /PLOT=BOXPLOT
 /STATISTICS=DESCRIPTIVES EXTREME(5)
 /MISSING=LISTWISE
 /NOTOTAL.

* No rows are removed automatically: extreme precipitation and wind can be valid weather observations.
SELECT IF (NOT MISSING(date) AND NOT MISSING(precipitation) AND NOT MISSING(temp_max) AND NOT MISSING(temp_min) AND NOT MISSING(wind) AND NOT MISSING(weather) AND invalid_numeric=0).
EXECUTE.

DELETE VARIABLES date_count duplicate_date invalid_numeric.
DATASET NAME WeatherClean.
SAVE OUTFILE='/Users/benjipro/Documents/Codex/2026-07-20/you-wrote-a-prompt-and-tested/outputs/applied-data-science-foundations/week-02-spss-data-quality-and-descriptive-statistics/data/Weather_Cleaned.sav'
 /COMPRESSED.
SAVE TRANSLATE OUTFILE='/Users/benjipro/Documents/Codex/2026-07-20/you-wrote-a-prompt-and-tested/outputs/applied-data-science-foundations/week-02-spss-data-quality-and-descriptive-statistics/data/Weather_Cleaned.csv'
 /TYPE=CSV
 /FIELDNAMES
 /REPLACE.
