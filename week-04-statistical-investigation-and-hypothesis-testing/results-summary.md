# Results Summary

The figures below were calculated directly from the supplied files. The SPSS syntax in `syntax/` is the reproducible workflow for the descriptive tables, outlier diagnostics, normality output, correlation tests, and charts. The normality screen reported here uses D'Agostino's K-squared test on the source values; the SPSS `EXAMINE` procedures additionally request histograms, normal probability plots, and the normality tests available in SPSS for each sample size.

## Salary data

### Data quality and descriptive results

- The raw workbook contains **6,704 rows**, **4,912 exact duplicate rows**, and missing values across all six columns.
- Retaining one copy of each duplicate and excluding incomplete records produces **1,787 complete observations**.
- Mean age is **35.14 years** (SD **8.21**), mean experience is **9.16 years** (SD **6.84**), and mean salary is **113,184.66** (SD **51,596.54**).
- IQR diagnostics flag **6** age values and **22** experience values; no salary values are outside the salary IQR fences. The values are retained because the checks alone do not show that they are errors.
- Age, experience, and salary each reject the strict normality screen (`p < .001`). The scatterplot and correlation result should therefore be interpreted alongside the distribution diagnostics rather than as evidence of a causal relationship.

### Hypothesis decision

Years of experience and salary have a strong positive Pearson association (**r = .819, p < .001, n = 1,787**). At the 5% level, reject H0. In this dataset, higher reported experience is associated with higher reported salary.

Age and experience are also very strongly associated (**r = .936, p < .001**). This matters when interpreting salary patterns: age and experience should not be treated as independent drivers without further modelling and diagnostic work.

## House-price data

### Data quality and descriptive results

- The file contains **21,613 observations**, with **no missing values**, **no duplicate rows**, and **no duplicate identifiers**.
- Mean sale price is **540,088.14** (SD **367,127.20**); mean living area is **2,079.90 sq ft** (SD **918.44**).
- IQR diagnostics flag **1,146** prices and **572** living-area values. These large or expensive homes are plausible observations and are retained.
- Price and living area reject the strict normality screen (`p < .001`), as do the other core numeric measures checked. This is expected in a large, skewed property dataset and is visible in the requested histograms, normal plots, and boxplots.

### Hypothesis decision

Sale price and living area have a strong positive Pearson association (**r = .702, p < .001, n = 21,613**). At the 5% level, reject H0. Homes with more living area tend to have higher sale prices in this dataset. This is an association only; it does not establish that additional floor area causes the price difference.

For context, grade is also strongly associated with price (**r = .667, p < .001**) and bathrooms show a moderate positive association (**r = .525, p < .001**).

## Daily weather data

### Data quality and descriptive results

- The workbook contains **1,461 daily observations**, with **no missing values**, **no duplicate rows**, and **no duplicate dates**.
- Mean precipitation is **3.03** (SD **6.68**), mean maximum temperature is **16.44** (SD **7.35**), mean minimum temperature is **8.23** (SD **5.02**), and mean wind speed is **3.24** (SD **1.44**).
- IQR diagnostics flag **206** precipitation values and **34** wind values, while neither temperature variable is outside its IQR fences. The flagged weather values are retained as potentially valid events.
- The numeric measures reject the strict normality screen (`p < .001`). The complete correlation table and scatterplot are therefore included so the direction, strength, and shape of the temperature relationship can be inspected.

### Hypothesis decision

Daily maximum and minimum temperature have a strong positive Pearson association (**r = .876, p < .001, n = 1,461**). At the 5% level, reject H0. Days with higher minimum temperatures tend also to have higher maximum temperatures in the supplied daily-weather record.

Maximum temperature has a small negative association with wind (**r = -.165, p < .001**). This result is descriptive of the observed period and should not be interpreted as a causal weather mechanism.
