* Week 4: House-price data statistical investigation.
* Update the file path before running this syntax in IBM SPSS Statistics.

GET DATA
 /TYPE=TXT
 /FILE='/Users/benjipro/Downloads/House_prices.csv'
 /ENCODING='UTF8'
 /DELCASE=LINE
 /DELIMITERS=','
 /QUALIFIER='"'
 /ARRANGEMENT=DELIMITED
 /FIRSTCASE=2
 /VARIABLES=
 id F12.0
 date A20
 price F12.2
 bedrooms F8.1
 bathrooms F8.2
 sqft_living F10.0
 sqft_lot F12.0
 floors F8.1
 waterfront F4.0
 view F4.0
 condition F4.0
 grade F4.0
 sqft_above F10.0
 sqft_basement F10.0
 yr_built F8.0
 yr_renovated F8.0
 zipcode F8.0
 lat F10.4
 long F10.4
 sqft_living15 F10.0
 sqft_lot15 F12.0.
EXECUTE.

DATASET NAME HousePrices.

* Missing-value profile.
FREQUENCIES VARIABLES=id price bedrooms bathrooms sqft_living sqft_lot floors waterfront view condition grade sqft_above sqft_basement yr_built yr_renovated zipcode lat long sqft_living15 sqft_lot15
 /STATISTICS=ALL
 /ORDER=ANALYSIS.

* Check the unique property identifier for duplicate records.
SORT CASES BY id(A).
AGGREGATE
 /OUTFILE=* MODE=ADDVARIABLES
 /BREAK=id
 /id_count=N.
COMPUTE duplicate_id=(id_count>1).
FREQUENCIES VARIABLES=id_count duplicate_id
 /ORDER=ANALYSIS.
DELETE VARIABLES id_count duplicate_id.

* Descriptive statistics and distribution plots for all quantitative measures.
EXAMINE VARIABLES=price bedrooms bathrooms sqft_living sqft_lot floors waterfront view condition grade sqft_above sqft_basement yr_built yr_renovated lat long sqft_living15 sqft_lot15
 /PLOT=BOXPLOT HISTOGRAM NPPLOT
 /STATISTICS=DESCRIPTIVES EXTREME(5)
 /CINTERVAL=95
 /MISSING=LISTWISE
 /NOTOTAL.

* Pearson correlation matrix and two-tailed significance tests.
* Research question: Is living area associated with sale price?
* H0: The population correlation between sqft_living and price is zero.
CORRELATIONS
 /VARIABLES=price bedrooms bathrooms sqft_living sqft_lot floors waterfront view condition grade sqft_above sqft_basement yr_built yr_renovated lat long sqft_living15 sqft_lot15
 /PRINT=TWOTAIL SIG FULL
 /MISSING=PAIRWISE.

* Graphical representation of the primary relationship.
GRAPH
 /SCATTERPLOT(BIVAR)=price WITH sqft_living
 /MISSING=LISTWISE.
