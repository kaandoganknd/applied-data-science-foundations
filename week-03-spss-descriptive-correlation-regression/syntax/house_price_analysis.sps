* House prices: descriptive statistics, correlation, and regression.
* Update the file path before running on another computer.

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

* Check duplicated identifiers and completeness before analysis.
FREQUENCIES VARIABLES=id price bedrooms bathrooms sqft_living sqft_lot floors waterfront view condition grade sqft_above sqft_basement yr_built yr_renovated zipcode lat long sqft_living15 sqft_lot15
 /STATISTICS=ALL
 /HISTOGRAM NORMAL
 /ORDER=ANALYSIS.

SORT CASES BY id(A).
AGGREGATE
 /OUTFILE=* MODE=ADDVARIABLES
 /BREAK=id
 /id_count=N.
COMPUTE duplicate_id=(id_count>1).
FREQUENCIES VARIABLES=id_count duplicate_id
 /FORMAT=NOTABLE
 /ORDER=ANALYSIS.
DELETE VARIABLES id_count duplicate_id.

CORRELATIONS
 /VARIABLES=price bedrooms bathrooms sqft_living sqft_lot floors waterfront view condition grade yr_built
 /PRINT=TWOTAIL SIG FULL
 /MISSING=PAIRWISE.

GRAPH
 /SCATTERPLOT(BIVAR)=price WITH sqft_living
 /MISSING=LISTWISE.
GRAPH
 /SCATTERPLOT(BIVAR)=price WITH grade
 /MISSING=LISTWISE.

REGRESSION
 /MISSING=LISTWISE
 /STATISTICS=COEFF OUTS R ANOVA CI(95) COLLIN TOL
 /CRITERIA=PIN(.05) POUT(.10)
 /NOORIGIN
 /DEPENDENT price
 /METHOD=ENTER sqft_living grade bathrooms waterfront view yr_built
 /SCATTERPLOT=(*ZPRED,*ZRESID)
 /RESIDUALS HISTOGRAM(ZRESID) NORMPROB(ZRESID).
