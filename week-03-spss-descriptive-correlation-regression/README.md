# SPSS Descriptive Statistics, Correlation and Regression

This project analyses three datasets in IBM SPSS Statistics:

- **Salary data** — descriptive statistics, correlations between age, experience and salary, and a multiple linear-regression model of salary.
- **House prices** — descriptive statistics, price correlations, and a multiple linear-regression model of house prices.
- **Daily weather** — descriptive statistics, correlations between weather measurements, and a regression model for daily maximum temperature.

## Analysis approach

The syntax requests all available descriptive measures for the numeric variables, scatterplots for the primary relationships, correlation matrices with two-tailed significance tests, and regression diagnostics.

The salary source contains many repeated rows. The syntax keeps one copy of every exact duplicate and excludes the small number of remaining incomplete records before analysis. The house-price and weather source files have no missing values or exact duplicate rows, so their observations are retained.

## Files

- `syntax/salary_analysis.sps`
- `syntax/house_price_analysis.sps`
- `syntax/weather_analysis.sps`
- `results-summary.md`
- `evidence/weather_analysis_output.spv` — previously saved SPSS Viewer output for the weather exploration and correlation work.

Raw datasets are not included. See `data/README.md` before running the syntax on another computer.
