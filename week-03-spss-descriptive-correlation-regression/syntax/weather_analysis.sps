* Daily weather: descriptive statistics, correlation, and regression.
* Update the file path before running on another computer.

GET DATA
 /TYPE=XLSX
 /FILE='/Users/benjipro/Downloads/weather.xlsx'
 /SHEET=name 'weather'
 /READNAMES=ON.
EXECUTE.

DATASET NAME WeatherWeek3.
FORMATS date (ADATE10) precipitation temp_max temp_min wind (F8.2).

FREQUENCIES VARIABLES=precipitation temp_max temp_min wind
 /STATISTICS=ALL
 /HISTOGRAM NORMAL
 /ORDER=ANALYSIS.
FREQUENCIES VARIABLES=weather
 /ORDER=ANALYSIS.

CORRELATIONS
 /VARIABLES=precipitation temp_max temp_min wind
 /PRINT=TWOTAIL SIG FULL
 /MISSING=PAIRWISE.

GRAPH
 /SCATTERPLOT(BIVAR)=temp_max WITH temp_min
 /MISSING=LISTWISE.
GRAPH
 /SCATTERPLOT(BIVAR)=temp_max WITH precipitation
 /MISSING=LISTWISE.

REGRESSION
 /MISSING=LISTWISE
 /STATISTICS=COEFF OUTS R ANOVA CI(95) COLLIN TOL
 /CRITERIA=PIN(.05) POUT(.10)
 /NOORIGIN
 /DEPENDENT temp_max
 /METHOD=ENTER temp_min precipitation wind
 /SCATTERPLOT=(*ZPRED,*ZRESID)
 /RESIDUALS HISTOGRAM(ZRESID) NORMPROB(ZRESID).
