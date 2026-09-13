# SPSS Statistical Investigation and Hypothesis Testing

This project develops a reproducible statistical investigation for three supplied datasets in IBM SPSS Statistics:

- **Salary data** — the relationship between experience and salary.
- **House-price data** — the relationship between living area and sale price.
- **Daily weather data** — the relationship between daily maximum and minimum temperature.

## What the analysis covers

For each dataset, the SPSS syntax performs:

1. missing-value and duplicate checks;
2. descriptive statistics;
3. outlier diagnostics with boxplots and extreme-value tables;
4. normality diagnostics with histograms, normal probability plots, and normality tests;
5. Pearson correlation analysis with two-tailed significance tests;
6. a scatterplot for the research-question relationship; and
7. an evidence-based decision on the stated null hypothesis.

Outliers are diagnosed rather than removed automatically. A value outside an interquartile-range fence may be a valid observation, so removal would require a documented data-quality or domain reason.

## Files

- `research-questions-and-hypotheses.md` — questions, null hypotheses, and decision rules.
- `results-summary.md` — source-data checks and concise interpretations.
- `syntax/salary_statistical_investigation.sps`
- `syntax/house_price_statistical_investigation.sps`
- `syntax/weather_statistical_investigation.sps`
- `data/README.md` — reproduction and data-handling notes.

The supplied source files are not committed because their redistribution terms are not established. Update the file paths at the top of each syntax file before running it locally in IBM SPSS Statistics.
