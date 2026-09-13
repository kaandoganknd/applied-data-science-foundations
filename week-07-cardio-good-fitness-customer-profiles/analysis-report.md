# Customer Profile Findings

## Data quality and sample

The dataset contains 180 purchase records: 80 TM195 customers, 60 TM498 customers, and 40 TM798 customers. There are no missing values or exact duplicate rows. Outlier diagnostics are included in the SPSS syntax. They are used to review unusual values, not to delete valid customer records automatically.

## Product-line profiles

| Product | N | Age | Education | Income | Usage | Fitness | Miles |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| TM195 | 80 | 28.55 | 15.04 | $46,418 | 3.09 | 2.96 | 82.79 |
| TM498 | 60 | 28.90 | 15.12 | $48,974 | 3.07 | 2.90 | 87.93 |
| TM798 | 40 | 29.10 | 17.32 | $75,442 | 4.78 | 4.63 | 166.90 |

Values are means. TM195 buyers are evenly split by gender. TM498 is also close to an even split. TM798 is 82.5% male in this sample, while its relationship-status distribution remains similar to the other product groups.

TM195 and TM498 have similar descriptive profiles. TM798 differs most clearly in income, education, planned use, expected mileage, and self-rated fitness. Its mean household income is about 60% above the TM195 mean, and its expected weekly mileage is roughly twice as high.

## Product associations

The Product × Gender chi-square test is significant, χ²(2) = 12.92, p = .002. Gender distribution therefore differs by product in this sample. The Product × Relationship Status result is not significant, χ²(2) = 0.08, p = .960.

Product × Fitness is strongly associated, χ²(8) = 118.78, p < .001. However, 3 of 15 expected frequencies are below 5. The result should be interpreted with this chi-square assumption in mind; the syntax also makes it easy to rerun the test after combining fitness categories if a robustness check is required.

One-way ANOVA finds no evidence of a mean age difference among the three products, F(2, 177) = 0.09, p = .910. Mean education, usage, and fitness differ across product lines (all p < .001). Levene's test indicates unequal variances for income and miles, so the Welch tests are the appropriate results for those outcomes: income, Welch's F(2, 85.53) = 43.65, p < .001; miles, Welch's F(2, 83.91) = 35.11, p < .001.

## Relationships among customer measures

Planned use, self-rated fitness, and expected mileage are strongly positively related: use and fitness, r = .669; use and miles, r = .759; fitness and miles, r = .786 (all p < .001). Income is positively associated with education (r = .626), expected mileage (r = .544), fitness (r = .535), and planned usage (r = .519), all p < .001. These findings describe relationships in the observed sample and do not establish cause and effect.

## Marketing implication

TM195 and TM498 can be addressed as general-fitness products, with the product choice likely to depend on features and price. TM798 should be positioned around higher-intensity use, performance, and durability. The low female share of TM798 buyers is a segment-development opportunity rather than evidence that the product should be marketed only to men.
