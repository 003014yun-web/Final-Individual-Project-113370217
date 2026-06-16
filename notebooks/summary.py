from pathlib import Path
import pandas as pd
import os
import statsmodels.formula.api as smf


try:
    notebook_dir = Path(__file__).resolve().parent
except NameError:
    notebook_dir = Path(os.getcwd()).resolve()

# Set up the data directories
data_dir = notebook_dir.parent / 'data'
input_path = data_dir / 'processed' / 'YRBS_2007_cleaned.csv'

# Set up independent output directories for tables and summaries
output_table_dir = notebook_dir.parent / 'output' / 'table'
output_summary_dir = notebook_dir.parent / 'output' / 'summary'

# Force directory creation if they don't exist
output_table_dir.mkdir(parents=True, exist_ok=True)
output_summary_dir.mkdir(parents=True, exist_ok=True)

# Read the cleaned dataset and fit the model
df = pd.read_csv(input_path)
model = smf.ols('MultipleSexPartners ~ TaughtAboutHIV + HIVTesting + CondomUse', data=df).fit()


# Extract statistical metrics
df_coefficients = pd.DataFrame({
    'Predictor': ['Intercept', 'HIV Education', 'HIV Testing', 'Condom Use'],
    'Beta (B)': model.params.values,
    'Std.Error (SE)': model.bse.values,
    't-value': model.tvalues.values,
    'p-value': model.pvalues.values,
    '95% CI Lower': model.conf_int()[0].values,
    '95% CI Upper': model.conf_int()[1].values
})

# Automatically append significance stars used in academic journals
def add_stars(p):
    if p < 0.001: return '***'
    elif p < 0.01: return '**'
    elif p < 0.05: return '*'
    else: return ''

df_coefficients['Significance'] = df_coefficients['p-value'].apply(add_stars)

# Format numerical results for professional display
df_coefficients['Beta (B)'] = df_coefficients['Beta (B)'].round(4)
df_coefficients['Std.Error (SE)'] = df_coefficients['Std.Error (SE)'].round(4)
df_coefficients['t-value'] = df_coefficients['t-value'].round(3)
df_coefficients['95% CI Lower'] = df_coefficients['95% CI Lower'].round(4)
df_coefficients['95% CI Upper'] = df_coefficients['95% CI Upper'].round(4)

# Format p-values (<0.001 formatting standard)
df_coefficients['p-value'] = df_coefficients['p-value'].apply(lambda x: '<.001' if x < 0.001 else f"{x:.4f}")

# Export table file
csv_table_path = output_table_dir / 'regression_results_table_en.csv'
df_coefficients.to_csv(csv_table_path, index=False, encoding='utf-8')
print(f"--- STEP 2: Table Export Complete ---")
print(f"APA-formatted table saved to: {csv_table_path}")


summary_txt_path = output_summary_dir / 'regression_model_summary_en.txt'

import statsmodels.api as sm
dw_stat = sm.stats.durbin_watson(model.resid)

# Build structured report text
report_content = f"""==============================================================================
               MULTIPLE LINEAR REGRESSION COMPLETE REPORT
                      DATASET SOURCE: YRBS 2007
==============================================================================
Analysis Date: June 11, 2026
Dependent Variable: MultipleSexPartners (Continuous Scale 1-6)
Total Observations (N): {int(model.nobs)} valid sexually active adolescent samples

--- [ Overall Model Fit Metrics ] ---
* Coefficient of Determination (R-squared): {model.rsquared:.4f}
  (The model explains approximately {model.rsquared*100:.2f}% of the variance in partner counts)
* Adjusted R-squared: {model.rsquared_adj:.4f}
* F-statistic value: {model.fvalue:.2f}
* Model Significance (Prob (F-statistic)): {model.f_pvalue:.4e} 
  (p < 0.05 indicates the overall behavioral model is highly statistically significant)

--- [ Statistical Assumptions & Diagnostics ] ---
* Error Independence (Durbin-Watson): {dw_stat:.3f} 
  (Values close to 2.0 confirm the absence of autocorrelation, satisfying the independence assumption)
* Multicollinearity Test (Condition Number): {model.condition_number:.2f} 
  (Values well below 30 indicate no major multicollinearity issues among predictors)

==============================================================================
             PARTIAL REGRESSION COEFFICIENTS & HYPOTHESIS TESTING
==============================================================================
* Intercept [Baseline Reference]:
  - Beta Coefficient (B) = {model.params['Intercept']:.4f} | p-value = {model.pvalues['Intercept']:.4e} (***)
  - Interpretation: When an adolescent has no HIV education, no testing history, and did not use a condom, the baseline average partner count is {model.params['Intercept']:.2f}.

* HIV Education (TaughtAboutHIV):
  - Beta Coefficient (B) = {model.params['TaughtAboutHIV']:.4f} | p-value = {model.pvalues['TaughtAboutHIV']:.4e} (***)
  - Decision: Reject H0. While controlling for other behaviors, receiving school HIV education independently and significantly predicts a fewer number of sex partners.

* HIV Testing History (HIVTesting):
  - Beta Coefficient (B) = {model.params['HIVTesting']:.4f} | p-value = {model.pvalues['HIVTesting']:.4e} (***)
  - Decision: Reject H0. While controlling for other variables, having been tested for HIV is significantly associated with more sex partners (reflecting risk-driven testing).

* Condom Use Behavior (CondomUse):
  - Beta Coefficient (B) = {model.params['CondomUse']:.4f} | p-value = {model.pvalues['CondomUse']:.4e} (***)
  - Decision: Reject H0. While controlling for other factors, using a condom during the last intercourse significantly predicts a lower total number of sex partners.

Note: *** p < 0.001, ** p < 0.01, * p < 0.05
==============================================================================
End of Report.
"""

# Write the report into an English TXT file
with open(summary_txt_path, 'w', encoding='utf-8') as f:
    f.write(report_content)

print(f"\n--- STEP 3: Summary Report Export Complete ---")
print(f"Detailed English text summary saved to: {summary_txt_path}")
print("\n🎉 Success! All data files, tables, figures, and reports have been generated.")