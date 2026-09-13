* Week 4: Salary data statistical investigation.
* Update the file path before running this syntax in IBM SPSS Statistics.

GET DATA
 /TYPE=XLSX
 /FILE='/Users/benjipro/Downloads/Salary_data.xlsx'
 /SHEET=name 'in'
 /READNAMES=ON.
EXECUTE.

DATASET NAME SalaryRaw.

* Missing-value profile before cleaning.
FREQUENCIES VARIABLES=Age Gender Education_Level Job_Title Years_of_Experience Salary
 /STATISTICS=ALL
 /ORDER=ANALYSIS.

* Identify exact duplicate records and retain one copy of each record.
SORT CASES BY Age(A) Gender(A) Education_Level(A) Job_Title(A) Years_of_Experience(A) Salary(A).
MATCH FILES
 /FILE=*
 /BY Age Gender Education_Level Job_Title Years_of_Experience Salary
 /FIRST=first_record.
COMPUTE duplicate_record=(NOT first_record).
FREQUENCIES VARIABLES=duplicate_record
 /ORDER=ANALYSIS.
SELECT IF first_record.
EXECUTE.

* Identify incomplete records after duplicate removal and exclude them from analysis.
COMPUTE incomplete_record=(MISSING(Age) OR MISSING(Gender) OR MISSING(Education_Level) OR MISSING(Job_Title) OR MISSING(Years_of_Experience) OR MISSING(Salary)).
FREQUENCIES VARIABLES=incomplete_record
 /ORDER=ANALYSIS.
SELECT IF NOT incomplete_record.
EXECUTE.
DELETE VARIABLES first_record duplicate_record incomplete_record.
DATASET NAME SalaryClean.

* Descriptive statistics for numeric and categorical variables.
FREQUENCIES VARIABLES=Age Years_of_Experience Salary
 /STATISTICS=ALL
 /HISTOGRAM NORMAL
 /ORDER=ANALYSIS.
FREQUENCIES VARIABLES=Gender Education_Level Job_Title
 /ORDER=ANALYSIS.

* Outlier and normality diagnostics; output includes boxplots, histograms,
* normal probability plots, descriptive statistics, extreme values, and tests of normality.
EXAMINE VARIABLES=Age Years_of_Experience Salary
 /PLOT=BOXPLOT HISTOGRAM NPPLOT
 /STATISTICS=DESCRIPTIVES EXTREME(5)
 /CINTERVAL=95
 /MISSING=LISTWISE
 /NOTOTAL.

* Pearson correlations with two-tailed significance tests.
* Research question: Is years of experience associated with salary?
* H0: The population correlation between years of experience and salary is zero.
CORRELATIONS
 /VARIABLES=Age Years_of_Experience Salary
 /PRINT=TWOTAIL SIG FULL
 /MISSING=PAIRWISE.

* Graphical representation of the primary relationship.
GRAPH
 /SCATTERPLOT(BIVAR)=Salary WITH Years_of_Experience
 /MISSING=LISTWISE.
