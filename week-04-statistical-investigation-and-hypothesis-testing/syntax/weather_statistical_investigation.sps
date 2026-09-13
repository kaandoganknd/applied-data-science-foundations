* Week 4: Daily weather statistical investigation.
* Update the file path before running this syntax in IBM SPSS Statistics.

GET DATA
 /TYPE=XLSX
 /FILE='/Users/benjipro/Downloads/weather.xlsx'
 /SHEET=name 'weather'
 /READNAMES=ON.
EXECUTE.

DATASET NAME WeatherWeek4.
FORMATS date (ADATE10) precipitation temp_max temp_min wind (F8.2).

* Missing-value profile.
FREQUENCIES VARIABLES=date precipitation temp_max temp_min wind weather
 /STATISTICS=ALL
 /ORDER=ANALYSIS.

* Check whether any dates occur more than once.
SORT CASES BY date(A).
AGGREGATE
 /OUTFILE=* MODE=ADDVARIABLES
 /BREAK=date
 /date_count=N.
COMPUTE duplicate_date=(date_count>1).
FREQUENCIES VARIABLES=date_count duplicate_date
 /ORDER=ANALYSIS.
DELETE VARIABLES date_count duplicate_date.

* Descriptive statistics, outlier diagnostics, and normality output.
EXAMINE VARIABLES=precipitation temp_max temp_min wind
 /PLOT=BOXPLOT HISTOGRAM NPPLOT
 /STATISTICS=DESCRIPTIVES EXTREME(5)
 /CINTERVAL=95
 /MISSING=LISTWISE
 /NOTOTAL.
FREQUENCIES VARIABLES=weather
 /ORDER=ANALYSIS.

* Pearson correlation matrix and two-tailed significance tests.
* Research question: Is daily minimum temperature associated with daily maximum temperature?
* H0: The population correlation between temp_min and temp_max is zero.
CORRELATIONS
 /VARIABLES=precipitation temp_max temp_min wind
 /PRINT=TWOTAIL SIG FULL
 /MISSING=PAIRWISE.

* Graphical representation of the primary relationship.
GRAPH
 /SCATTERPLOT(BIVAR)=temp_max WITH temp_min
 /MISSING=LISTWISE.
