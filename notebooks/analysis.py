from pathlib import Path
import pandas as pd
import os
import statsmodels.formula.api as smf


try:
    notebook_dir = Path(__file__).resolve().parent
except NameError:
    notebook_dir = Path(os.getcwd()).resolve()

data_dir = notebook_dir.parent / 'data' 
input_path = data_dir / 'processed' / 'YRBS_2007_cleaned.csv'

print(f"--- 步驟 1: 讀取分析資料 ---")
print(f"正在讀取已清理的檔案: {input_path}")

df_cleaned = pd.read_csv(input_path)
print(f"成功載入資料！可分析的有效樣本數: {df_cleaned.shape[0]} 筆\n")

print("\nGroup counts:")
print(df_cleaned['TaughtAboutHIV'].value_counts())
print(df_cleaned['HIVTesting'].value_counts())
print(df_cleaned['CondomUse'].value_counts())

print("\nDescriptive statistics:")
print(df_cleaned[['MultipleSexPartners','TaughtAboutHIV',
'HIVTesting','CondomUse']].describe())

print(df_cleaned['MultipleSexPartners'].value_counts().sort_index())

model = smf.ols('MultipleSexPartners ~ TaughtAboutHIV + HIVTesting + CondomUse', data=df_cleaned).fit()


print("\n==============================================================================")
print("                    MULTIPLE LINEAR REGRESSION RESULTS                        ")
print("==============================================================================")
print(model.summary())
print("==============================================================================\n")


print(f"--- 步驟 4: 報告核心指標摘要 ---")
print(f"模型解釋度 (R-squared): {model.rsquared:.4f} (代表這些行為能解釋青少年伴侶數量 {model.rsquared*100:.2f}% 的變異)")
print(f"模型顯著性 (F-statistic p-value): {model.f_pvalue:.4e}")
print("\n各變數之偏迴歸係數與顯著性檢定：")
for var in ['Intercept', 'TaughtAboutHIV', 'HIVTesting', 'CondomUse']:
    coef = model.params[var]
    p_val = model.pvalues[var]
    sig_status = "★ 顯著 (p < 0.05)" if p_val < 0.05 else "不顯著 (p >= 0.05)"
    print(f" - {var:<15} : 係數(Beta) = {coef:>7.4f} | p-value = {p_val:>8.4e} | {sig_status}")