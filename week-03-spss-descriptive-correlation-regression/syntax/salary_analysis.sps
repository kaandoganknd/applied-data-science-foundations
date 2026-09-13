* Salary data: descriptive statistics, correlation, and regression.
* Update the file path before running on another computer.

GET DATA
 /TYPE=XLSX
 /FILE='/Users/benjipro/Downloads/Salary_data.xlsx'
 /SHEET=name 'in'
 /READNAMES=ON.
EXECUTE.

DATASET NAME SalaryRaw.

* Keep one copy of each exact duplicate record.
SORT CASES BY Age(A) Gender(A) Education_Level(A) Job_Title(A) Years_of_Experience(A) Salary(A).
MATCH FILES
 /FILE=*
 /BY Age Gender Education_Level Job_Title Years_of_Experience Salary
 /FIRST=first_record.
SELECT IF first_record.
EXECUTE.

* Remove incomplete records before calculation.
SELECT IF NOT (MISSING(Age) OR MISSING(Gender) OR MISSING(Education_Level) OR MISSING(Job_Title) OR MISSING(Years_of_Experience) OR MISSING(Salary)).
EXECUTE.
DELETE VARIABLES first_record.
DATASET NAME SalaryClean.

FREQUENCIES VARIABLES=Age Years_of_Experience Salary
 /STATISTICS=ALL
 /HISTOGRAM NORMAL
 /ORDER=ANALYSIS.
FREQUENCIES VARIABLES=Gender Education_Level Job_Title
 /ORDER=ANALYSIS.

CORRELATIONS
 /VARIABLES=Age Years_of_Experience Salary
 /PRINT=TWOTAIL SIG FULL
 /MISSING=PAIRWISE.

GRAPH
 /SCATTERPLOT(BIVAR)=Salary WITH Years_of_Experience
 /MISSING=LISTWISE.
GRAPH
 /SCATTERPLOT(BIVAR)=Salary WITH Age
 /MISSING=LISTWISE.

REGRESSION
 /MISSING=LISTWISE
 /STATISTICS=COEFF OUTS R ANOVA CI(95) COLLIN TOL
 /CRITERIA=PIN(.05) POUT(.10)
 /NOORIGIN
 /DEPENDENT Salary
 /METHOD=ENTER Years_of_Experience Age
 /SCATTERPLOT=(*ZPRED,*ZRESID)
 /RESIDUALS HISTOGRAM(ZRESID) NORMPROB(ZRESID).
