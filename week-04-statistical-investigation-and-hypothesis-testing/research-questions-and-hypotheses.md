# Research Questions and Hypotheses

All inferential tests use a two-tailed Pearson correlation at a 5% significance level. A result with `p < .05` leads to rejection of the null hypothesis. Correlation describes association; it does not establish a causal effect.

## Salary data

**Research question:** Is years of professional experience associated with salary in the cleaned salary dataset?

**H0:** The population correlation between years of experience and salary is zero.

**H1:** The population correlation between years of experience and salary is not zero.

The analysis first removes exact duplicate records and then excludes incomplete records. This is necessary because the original source contains repeated rows and missing values.

## House-price data

**Research question:** Is living area (`sqft_living`) associated with sale price in the supplied house-price dataset?

**H0:** The population correlation between living area and sale price is zero.

**H1:** The population correlation between living area and sale price is not zero.

The dataset is retained as supplied after checking for missing values and duplicate identifiers. High-price and large-home observations are diagnosed as possible outliers, not deleted by default.

## Daily weather data

**Research question:** Is daily minimum temperature associated with daily maximum temperature?

**H0:** The population correlation between daily minimum and maximum temperature is zero.

**H1:** The population correlation between daily minimum and maximum temperature is not zero.

The daily observations are retained after missing-value and duplicate-date checks. Rainfall and wind observations flagged by boxplots are reviewed as potentially valid weather events rather than automatically removed.
