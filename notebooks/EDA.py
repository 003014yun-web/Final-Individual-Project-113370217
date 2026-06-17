from pathlib import Path
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.formula.api as smf

try:
    notebook_dir = Path(__file__).resolve().parent
except NameError:
    notebook_dir = Path(os.getcwd()).resolve()

data_dir = notebook_dir.parent / 'data'
input_path = data_dir / 'processed' / 'YRBS_2007_cleaned.csv'

output_fig_dir = notebook_dir.parent / 'output' / 'figure'
output_fig_dir.mkdir(parents=True, exist_ok=True)


df = pd.read_csv(input_path)

model = smf.ols('MultipleSexPartners ~ TaughtAboutHIV + HIVTesting + CondomUse', data=df).fit()

sns.set_theme(style="whitegrid")
plt.rcParams['font.sans-serif'] = ['Arial', 'Microsoft JhengHei'] # 確保中英文相容
plt.rcParams['axes.unicode_minus'] = False 

plt.figure(figsize=(9, 5))

variables = ['TaughtAboutHIV', 'HIVTesting', 'CondomUse']
coefs = model.params[variables]
conf_int = model.conf_int().loc[variables]

for i, var in enumerate(variables):
    plt.errorbar(x=coefs[var], y=i, xerr=[[coefs[var] - conf_int.loc[var, 0]], [conf_int.loc[var, 1] - coefs[var]]],
                 fmt='o', color='#2b5c8f', markersize=8, capsize=5, elinewidth=2)

plt.axvline(x=0, color='red', linestyle='--', linewidth=1.2, label='No Effect Line')

plt.yticks(range(len(variables)), ['HIV Education', 'HIV Testing', 'Condom Use '], fontsize=11)
plt.xlabel('Regression Coefficient (Beta Coefficient)', fontsize=12)
plt.title('Figure 1: Forest Plot of HIV-Related Predictors on Number of Sex Partners\n(95% Confidence Intervals)', fontsize=13, pad=15)
plt.grid(True, linestyle=':', alpha=0.6)

fig1_path = output_fig_dir / 'regression_forest_plot.png'
plt.tight_layout()
plt.savefig(fig1_path, dpi=300)
plt.close()
print(f"成功儲存圖表一至: {fig1_path}")

plot_data = []
for var, name in [('TaughtAboutHIV', 'HIV Education'), ('HIVTesting', 'HIV Testing'), ('CondomUse', 'Condom Use')]:
    for status in [0, 1]:
        mean_val = df[df[var] == status]['MultipleSexPartners'].mean()
        status_name = 'Yes (1)' if status == 1 else 'No (0)'
        plot_data.append({'Variable': name, 'Status': status_name, 'MeanPartners': mean_val})

df_plot = pd.DataFrame(plot_data)

plt.figure(figsize=(9, 5.5))
ax = sns.barplot(x='Variable', y='MeanPartners', hue='Status', data=df_plot, palette='Blues_r')

for p in ax.patches:
    if p.get_height() > 0:
        ax.annotate(f"{p.get_height():.2f}", 
                    (p.get_x() + p.get_width() / 2., p.get_height()), 
                    ha='center', va='center', 
                    xytext=(0, 8), 
                    textcoords='offset points', fontsize=10, weight='bold')


plt.xlabel('Behavioral and Educational Variables', fontsize=12)
plt.ylabel('Average Number of Sex Partners (1-6 Scale)', fontsize=12)
plt.title('Figure 2: Comparison of Average Sex Partner Counts by Behavior Categories', fontsize=13, pad=15)
plt.ylim(0, 4.0) # 留點空間給標籤
plt.legend(title='Status', loc='upper right')

fig2_path = output_fig_dir / 'behavior_comparison_barplot.png'
plt.tight_layout()
plt.savefig(fig2_path, dpi=300)
plt.close()
print(f"成功儲存圖表二至: {fig2_path}")

print("\n🎉 所有圖表繪製完成！請至 output/figure 資料夾內查看。")