from pathlib import Path
import pandas as pd
import os

try:
    notebook_dir = Path(__file__).resolve().parent
except NameError:
    notebook_dir = Path(os.getcwd()).resolve()

print(f"--- 步驟 1: 路径確認 ---")
print(f"當前 Notebook 所在位置: {notebook_dir}")

data_dir = notebook_dir.parent / 'data' 

input_path = data_dir / 'raw' / 'YRBS_2007.csv'
output_dir = data_dir / 'processed'
output_path = output_dir / 'YRBS_2007_cleaned.csv'

print(f"預期讀取原始檔案路徑: {input_path}")
print(f"預期儲存清理檔案路徑: {output_path}")


output_dir.mkdir(parents=True, exist_ok=True)

try:
    df = pd.read_csv(input_path)
    print("\n--- 步驟 2: 成功讀取原始資料 ---")
    print(f"原始資料筆數: {df.shape[0]} 筆")
except FileNotFoundError:
    print(f"\n❌ 錯誤：找不到原始檔案！請檢查該路徑下是否有檔案: {input_path}")
    print("請修改程式碼第 20 行的 'data_dir' 設定，指向正確的 data 資料夾。")
    raise

def process_taught_hiv(val):
    if val == 1: return 1
    elif val == 2: return 0
    else: return None
df['TaughtAboutHIV'] = df['TaughtAboutHIV'].apply(process_taught_hiv)

def process_hiv_testing(val):
    if val == 1: return 1
    elif val == 2: return 0
    else: return None
df['HIVTesting'] = df['HIVTesting'].apply(process_hiv_testing)

def process_condom_use(val):
    if val == 2: return 1
    elif val == 3: return 0
    else: return None 
df['CondomUse'] = df['CondomUse'].apply(process_condom_use)

def process_multiple_sex_partners(val):
    if val in [1, 2]: return None 
    elif 3 <= val <= 8: return val - 2 
    else: return None
df['MultipleSexPartners'] = df['MultipleSexPartners'].apply(process_multiple_sex_partners)


df = df.dropna(subset=['MultipleSexPartners', 'CondomUse', 'TaughtAboutHIV', 'HIVTesting'])

df.to_csv(output_path, index=False)

print(f"\n--- 步驟 3: 資料清理與儲存成功 ---")
print(f"成功將清理後的資料存入目標資料夾！")
print(f"最終存檔路徑: {output_path}")
print(f"清理後的資料集維度: {df.shape}")