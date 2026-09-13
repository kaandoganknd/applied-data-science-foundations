* Week 2 individual practical: Iris data quality and cleaning.
* Update the two file paths before running this syntax on another computer.

GET DATA
 /TYPE=TXT
 /FILE='/Users/benjipro/Downloads/Iris_Modified.csv'
 /ENCODING='UTF8'
 /DELCASE=LINE
 /DELIMITED
 /QUALIFIER='"'
 /ARRANGEMENT=DELIMITED
 /FIRSTCASE=2
 /IMPORTCASE=ALL
 /VARIABLES=
 Id F8.0
 SepalLengthCm F8.2
 SepalWidthCm F8.2
 PetalLengthCm F8.2
 PetalWidthCm F8.2
 Species A20.
EXECUTE.

DATASET NAME IrisRaw.
VARIABLE LABELS
 Id 'Record identifier'
 SepalLengthCm 'Sepal length in centimetres'
 SepalWidthCm 'Sepal width in centimetres'
 PetalLengthCm 'Petal length in centimetres'
 PetalWidthCm 'Petal width in centimetres'
 Species 'Iris species'.
FORMATS Id (F8.0) SepalLengthCm SepalWidthCm PetalLengthCm PetalWidthCm (F8.2).

* Initial audit: missing values and descriptive statistics.
FREQUENCIES VARIABLES=Id SepalLengthCm SepalWidthCm PetalLengthCm PetalWidthCm Species
 /FORMAT=NOTABLE
 /ORDER=ANALYSIS.
DESCRIPTIVES VARIABLES=SepalLengthCm SepalWidthCm PetalLengthCm PetalWidthCm
 /STATISTICS=MEAN STDDEV MIN MAX.

* Identify duplicated record identifiers.
SORT CASES BY Id(A).
AGGREGATE
 /OUTFILE=* MODE=ADDVARIABLES
 /BREAK=Id
 /id_count=N.
COMPUTE duplicate_id=(id_count>1).
FREQUENCIES VARIABLES=id_count duplicate_id
 /FORMAT=NOTABLE
 /ORDER=ANALYSIS.

* Review potential outliers with boxplots and extreme values.
EXAMINE VARIABLES=SepalLengthCm SepalWidthCm PetalLengthCm PetalWidthCm
 /PLOT=BOXPLOT
 /STATISTICS=DESCRIPTIVES EXTREME(5)
 /MISSING=LISTWISE
 /NOTOTAL.

* Keep one observation for each duplicated identifier.
SORT CASES BY Id(A).
MATCH FILES
 /FILE=*
 /BY Id
 /FIRST=first_id.
SELECT IF first_id.
EXECUTE.

* Impute the six missing measurements with the median within each species.
SORT CASES BY Species(A).
AGGREGATE
 /OUTFILE=* MODE=ADDVARIABLES
 /BREAK=Species
 /median_sepal_width=MEDIAN(SepalWidthCm)
 /median_petal_length=MEDIAN(PetalLengthCm).
IF MISSING(SepalWidthCm) SepalWidthCm=median_sepal_width.
IF MISSING(PetalLengthCm) PetalLengthCm=median_petal_length.
EXECUTE.

* Recheck the cleaned data. IQR flags are reviewed, not removed automatically.
FREQUENCIES VARIABLES=Id SepalLengthCm SepalWidthCm PetalLengthCm PetalWidthCm Species
 /FORMAT=NOTABLE
 /ORDER=ANALYSIS.
EXAMINE VARIABLES=SepalLengthCm SepalWidthCm PetalLengthCm PetalWidthCm
 /PLOT=BOXPLOT
 /STATISTICS=DESCRIPTIVES EXTREME(5)
 /MISSING=LISTWISE
 /NOTOTAL.

DELETE VARIABLES id_count duplicate_id first_id median_sepal_width median_petal_length.
DATASET NAME IrisClean.
SAVE OUTFILE='/Users/benjipro/Documents/Codex/2026-07-20/you-wrote-a-prompt-and-tested/outputs/applied-data-science-foundations/week-02-spss-data-quality-and-descriptive-statistics/data/Iris_Cleaned.sav'
 /COMPRESSED.
SAVE TRANSLATE OUTFILE='/Users/benjipro/Documents/Codex/2026-07-20/you-wrote-a-prompt-and-tested/outputs/applied-data-science-foundations/week-02-spss-data-quality-and-descriptive-statistics/data/Iris_Cleaned.csv'
 /TYPE=CSV
 /FIELDNAMES
 /REPLACE.
