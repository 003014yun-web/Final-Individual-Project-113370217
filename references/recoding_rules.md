# Recoding Rules

## Variable Coding

The original YRBS responses were recoded for regression analysis.

---

# TaughtAboutHIV

Original coding:

- Yes = 1
- No = 2
- Not sure = 3

Recoding:

- Yes → 1
- No → 0
- Not sure → Missing

---

# HIVTesting

Original coding:

- Yes = 1
- No = 2
- Not sure = 3

Recoding:

- Yes → 1
- No → 0
- Not sure → Missing

---

# CondomUse

Original coding:

- Never had sexual intercourse = 1
- Yes = 2
- No = 3

Recoding:

- Yes → 1
- No → 0
- Never had sexual intercourse → Missing

---

# MultipleSexPartners

Original coding:

- Never had sexual intercourse = 1
- 1 person = 2
- 2 people = 3
- 3 people = 4
- 4 people = 5
- 5 people = 6
- 6 or more people = 7

Recoding:

- Never had sexual intercourse → Missing
- 1 person → Missing
- 2 or more people → Numerical scale

---

# Missing Values

Observations with missing values in the following variables were removed:

- MultipleSexPartners
- CondomUse
- TaughtAboutHIV
- HIVTesting

---

# Method Choice

Multiple Linear Regression (OLS) was selected because:

- The response variable was treated as quantitative.
- Multiple predictors were analyzed simultaneously.
- The model estimates the association between HIV-related behaviors and sexual partner numbers.

---

# Assumptions Considered

The following assumptions were considered:

- Linear relationship.
- Independence of observations.
- No severe multicollinearity.
- Homoscedasticity.
- Approximate normality of residuals.

The large sample size supports the robustness of the regression estimates.
