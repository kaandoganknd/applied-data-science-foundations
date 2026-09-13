* CardioGood Fitness customer profiles.
* Update the file path before running this syntax in IBM SPSS Statistics.

GET DATA
 /TYPE=TXT
 /FILE='/Users/benjipro/Downloads/CardioGoodFitness.csv'
 /ENCODING='UTF8'
 /DELCASE=LINE
 /DELIMITERS=','
 /QUALIFIER='"'
 /ARRANGEMENT=DELIMITED
 /FIRSTCASE=2
 /VARIABLES=
 Product A5
 Age F8.0
 Gender A6
 Education F8.0
 MaritalStatus A10
 Usage F8.0
 Fitness F8.0
 Income F12.0
 Miles F8.0.
EXECUTE.

DATASET NAME CardioGoodFitness.

VARIABLE LABELS
 Product 'Purchased treadmill product'
 Age 'Customer age in years'
 Gender 'Customer gender'
 Education 'Years of education'
 MaritalStatus 'Relationship status'
 Usage 'Planned treadmill sessions per week'
 Fitness 'Self-rated fitness from 1 poor to 5 excellent'
 Income 'Annual household income in dollars'
 Miles 'Expected weekly walking or running miles'.

VALUE LABELS Fitness
 1 'Poor'
 2 'Fair'
 3 'Average'
 4 'Good'
 5 'Excellent'.

VARIABLE LEVEL Product Gender MaritalStatus (NOMINAL)
 Age Education Usage Income Miles (SCALE)
 Fitness (ORDINAL).

* Data-quality profile: missing values, value distributions, and exact duplicates.
FREQUENCIES VARIABLES=Product Age Gender Education MaritalStatus Usage Fitness Income Miles
 /STATISTICS=ALL
 /ORDER=ANALYSIS.

SORT CASES BY Product(A) Age(A) Gender(A) Education(A) MaritalStatus(A) Usage(A) Fitness(A) Income(A) Miles(A).
MATCH FILES
 /FILE=*
 /BY Product Age Gender Education MaritalStatus Usage Fitness Income Miles
 /FIRST=first_record.
COMPUTE exact_duplicate=(NOT first_record).
FREQUENCIES VARIABLES=exact_duplicate
 /ORDER=ANALYSIS.
DELETE VARIABLES first_record exact_duplicate.

* Outlier and distribution diagnostics for all numeric customer measures.
EXAMINE VARIABLES=Age Education Usage Fitness Income Miles
 /PLOT=BOXPLOT HISTOGRAM NPPLOT
 /STATISTICS=DESCRIPTIVES EXTREME(5)
 /CINTERVAL=95
 /MISSING=LISTWISE
 /NOTOTAL.

* Descriptive customer profiles by treadmill product line.
MEANS TABLES=Age Education Usage Fitness Income Miles BY Product
 /CELLS=COUNT MEAN STDDEV MIN MAX.

CROSSTABS
 /TABLES=Product BY Gender
 /STATISTICS=CHISQ PHI
 /CELLS=COUNT ROW COLUMN EXPECTED.

CROSSTABS
 /TABLES=Product BY MaritalStatus
 /STATISTICS=CHISQ PHI
 /CELLS=COUNT ROW COLUMN EXPECTED.

CROSSTABS
 /TABLES=Product BY Fitness
 /STATISTICS=CHISQ PHI
 /CELLS=COUNT ROW COLUMN EXPECTED.

* Convert product names to numeric codes for one-way ANOVA.
RECODE Product ('TM195'=1) ('TM498'=2) ('TM798'=3) INTO Product_Code.
VARIABLE LABELS Product_Code 'Purchased treadmill product code'.
VALUE LABELS Product_Code 1 'TM195' 2 'TM498' 3 'TM798'.
VARIABLE LEVEL Product_Code (NOMINAL).
EXECUTE.

* Group comparison results: descriptive measures, Levene's test, ANOVA, Welch, Tukey, and Games-Howell.
ONEWAY Age Education Usage Fitness Income Miles BY Product_Code
 /STATISTICS DESCRIPTIVES HOMOGENEITY WELCH
 /MISSING ANALYSIS
 /POSTHOC=TUKEY GH ALPHA(.05).

* Pearson correlations among continuous customer measures.
CORRELATIONS
 /VARIABLES=Age Education Usage Fitness Income Miles
 /PRINT=TWOTAIL SIG FULL
 /MISSING=PAIRWISE.

* Graphical summaries for the product profiles and principal relationships.
GRAPH
 /BAR(GROUPED)=COUNT BY Product BY Gender.
GRAPH
 /BAR(SIMPLE)=MEAN(Income) BY Product.
GRAPH
 /BAR(SIMPLE)=MEAN(Usage) BY Product.
GRAPH
 /BAR(SIMPLE)=MEAN(Fitness) BY Product.
GRAPH
 /BAR(SIMPLE)=MEAN(Miles) BY Product.
GRAPH
 /SCATTERPLOT(BIVAR)=Miles WITH Usage
 /MISSING=LISTWISE.
GRAPH
 /SCATTERPLOT(BIVAR)=Income WITH Education
 /MISSING=LISTWISE.
