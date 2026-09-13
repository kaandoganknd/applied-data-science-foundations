# Results Summary

The values below were checked against the supplied source datasets. The SPSS syntax reproduces the descriptive outputs, correlation tables, scatterplots, regression tables and residual diagnostics.

## Salary data

- The original file has **6,704 rows**. Removing **4,912 exact duplicate rows** and five incomplete records leaves **1,787 observations** for analysis.
- Mean salary is **113,184.66**, with a standard deviation of **51,596.54**. Mean age is **35.14** years and mean experience is **9.16** years.
- Salary has a strong positive Pearson correlation with years of experience (**r = .819**) and a smaller positive correlation with age (**r = .767**).
- The regression model using experience and age explains **67.0%** of salary variation (`R² = .670`). Experience is a positive predictor; age adds little after experience is included because the two predictors are highly correlated (`r = .936`).

## House prices

- The dataset contains **21,613 observations**, with no missing values or exact duplicate rows.
- Mean price is **540,088.14**. The strongest listed bivariate association with price is living area (`sqft_living`, **r = .702**), followed by grade (**r = .667**) and bathrooms (**r = .525**).
- A model containing living area, grade, bathrooms, waterfront status, view, and year built explains **64.4%** of price variation (`R² = .644`). These are associations in the supplied dataset, not causal effects.

## Daily weather

- The dataset contains **1,461 daily observations** with no missing values, duplicate dates, or invalid values where maximum temperature is below minimum temperature.
- Mean precipitation is **3.03**, mean maximum temperature is **16.44**, mean minimum temperature is **8.23**, and mean wind speed is **3.24**.
- Maximum and minimum temperature show a strong positive correlation (**r = .876**). Precipitation has a modest negative correlation with maximum temperature (**r = -.229**).
- The model using minimum temperature, precipitation, and wind explains **79.7%** of the observed variation in maximum temperature (`R² = .797`). The included SPSS Viewer file preserves the earlier descriptive and correlation output; the Week 3 syntax adds the regression workflow.
