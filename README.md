## 💾 使用數據 / Dataset

* **數據集名稱 / Dataset Name**: 
  * 2007 Youth Risk Behavior Surveillance System (YRBSS)
* **來源 / Source**: 
  * Centers for Disease Control and Prevention (CDC)

---

## 🔍 選定變數與資料清洗 / Selected Variables & Data Cleaning

### 
本研究聚焦於**已具備性經驗的青少年群體**，探討其愛滋病相關衛教、篩檢行為、安全防護措施對其性伴侶數量的預測效果。根據 Python 清洗邏輯，原始 YRBSS 數據的處理與重碼細節如下：

### 
This study focuses on **sexually active adolescents** to evaluate the predictive effects of HIV education, HIV testing history, and protective behaviors on their total number of sex partners. According to our Python data cleaning logic, the original YRBSS variables are processed and recoded as follows:

---

### 1. 依變數：近期性伴侶數量 / Dependent Variable: Number of Sex Partners (`MultipleSexPartners`)

  * **原始欄位**: `BL`（過去 3 個月內的性伴侶人數，原始編碼為 1 至 8）。
  * **資料篩選**: 剔除原始編碼為 `1`（從未發生過性行為）與 `2`（過去 3 個月內無性行為）的樣本，**僅保留具備活躍性經驗之青少年**。
  * **連續變數轉換**: 為了符合線性迴歸之連續型變數假設，將原始代碼進行減 2 映射（`val - 2`），轉換為具有實質數量意義的**連續數值 1 至 6 人**（其中 `6` 代表 6 人或以上）。
  * 異常值、漏填或不確定之回答皆轉為 `None`（缺失值）。

  * **Original Variable**: `Q61` (Number of sex partners during the past 3 months, originally coded from 1 to 8).
  * **Sample Filtering**: Excluded records coded as `1` (Never had sexual intercourse) and `2` (No sex partners during the past 3 months) to **specifically target sexually active adolescents**.
  * **Continuous Variable Scaling**: To satisfy the continuous variable assumption of linear regression, the original codes are mapped by subtracting 2 (`val - 2`), converting them into a **continuous numerical scale from 1 to 6** (where `6` indicates 6 or more partners).
  * Refusals, missing data, or "Not sure" responses are converted to `None` (Missing values).

### 2. 自變數 A：學校愛滋病衛教認知 / Independent Variable A: HIV Education (`TaughtAboutHIV`)

  * **原始欄位**: `CH`（是否曾在學校上過關於愛滋病的衛教課程）。
  * **重碼邏輯**: `1` (Yes) 代表曾接受過學校愛滋病衛教（原編碼 1）；`0` (No) 代表未曾接受過學校愛滋病衛教（原編碼 2）。原編碼 3（Not sure）或漏填者皆轉為 `None`。

  * **Original Variable**: `Q85` (Ever taught about AIDS or HIV infection in school).
  * **Recoding Logic**: `1` (Yes) indicates having received HIV education in school (originally 1); `0` (No) indicates never received HIV education in school (originally 2). Responses with code 3 (Not sure) or missing are converted to `None`.

### 3. 自變數 B：愛滋病篩檢行為 / Independent Variable B: HIV Testing (`HIVTesting`)

  * **原始欄位**: `CQ`（是否曾接受過愛滋病病毒/HIV 檢測）。
  * **重碼邏輯**: `1` (Yes) 代表曾做過愛滋病篩檢（原編碼 1）；`0` (No) 代表未曾做過愛滋病篩檢（原編碼 2）。原編碼 3（Not sure）或漏填者皆轉為 `None`。

  * **Original Variable**: `Q94` (Ever been tested for HIV).
  * **Recoding Logic**: `1` (Yes) indicates having been tested for HIV (originally 1); `0` (No) indicates never been tested for HIV (originally 2). Responses with code 3 (Not sure) or missing are converted to `None`.

### 4. 自變數 C：安全防護行為 / Independent Variable C: Condom Use (`CondomUse`)

  * **原始欄位**: `BL`（最近一次性行為中是否有使用保險套）。
  * **重碼邏輯**: `1` (Yes) 代表最近一次性行為有使用保險套（原編碼 2）；`0` (No) 代表最近一次性行為未使用保險套（原編碼 3）。原編碼 1（從未發生過性行為者，已於前置步驟預先剔除）或其他無效值皆轉為 `None`。

  * **Original Variable**: `Q63` (Used a condom during last sexual intercourse).
  * **Recoding Logic**: `1` (Yes) indicates a condom was used during the last sexual intercourse (originally 2); `0` (No) indicates a condom was not used (originally 3). Code 1 (Never had sex) is pre-filtered, and other invalid responses are converted to `None`.

### ⚠️ 缺失值處理 / Missing Data Handling (Listwise Deletion)
* **中文**: 程式碼最後使用 `dropna(subset=[...])` 進行列刪除法，確保進入迴歸模型分析的每一個青少年觀測值，皆具備上述四個核心欄位的完整回答，以避免缺失值干擾統計推論。
* **English**: The script applies listwise deletion via `dropna(subset=[...])` to ensure that every adolescent observation entered into the regression model contains complete records for all four core variables, preventing missing data from confounding the statistical inference.

---

## 📊 統計檢定方法 / Statistical Methodology

### 
本研究採用 **多元線性迴歸分析 (Multiple Linear Regression)** 進行統計建模，以評估多個二分（Dummy）預測因子對於連續型結果變數的共同預測力與相對貢獻度。

* **統計模型方程式**:
  $$\text{MultipleSexPartners} = \beta_0 + \beta_1(\text{TaughtAboutHIV}) + \beta_2(\text{HIVTesting}) + \beta_3(\text{CondomUse}) + \epsilon$$
  
* **分析重點**:
  1. **整體模型顯著性**: 檢視 $F$-test 與 $R^2$ 決定係數，評估該行為模型對青少年性伴侶數量的解釋能力。
  2. **偏迴歸係數 ($\beta$) 檢定**: 透過 $t$-test 評估在控制其他變數不變下，單一預測因子對伴侶數量的獨立影響是否顯著 ($p < 0.05$)。

### 
This study utilizes **Multiple Linear Regression Analysis** for statistical modeling to evaluate the collective predictive power and unique contributions of multiple dichotomous (dummy) predictors on a continuous outcome variable.

* **Statistical Model Equation**:
  $$\text{MultipleSexPartners} = \beta_0 + \beta_1(\text{TaughtAboutHIV}) + \beta_2(\text{HIVTesting}) + \beta_3(\text{CondomUse}) + \epsilon$$
  
* **Analytical Focus**:
  1. **Overall Model Significance**: Examine the $F$-statistic and the Coefficient of Determination ($R^2$) to evaluate the explanatory power of the behavioral model on adolescents' number of sex partners.
  2. **Partial Regression Coefficient ($\beta$) Testing**: Utilize $t$-tests to evaluate whether each individual predictor significantly affects the number of partners ($p < 0.05$) while controlling for other variables in the model.

---

## ❓ 研究問題與統計假設 / Project Questions & Hypotheses

### 📌 1. 學校愛滋病衛教對性伴侶數量的預測效果 / Predictive Effect of School HIV Education
* **中文**: 在控制篩檢行為與保險套使用情況下，曾接受學校愛滋病衛教是否能顯著預測青少年擁有較少的性伴侶數量？
* **English**: Does receiving HIV education in school significantly predict a lower number of sex partners among sexually active adolescents, after controlling for testing and protective behaviors?
* **假設檢定 / Hypotheses**:
  * $H_0: \beta_1 = 0$ （學校衛教對性伴侶數量沒有顯著預測效果 / HIV education does not significantly predict the number of sex partners.）
  * $H_1: \beta_1 \neq 0$ （學校衛教對性伴侶數量具有顯著預測效果 / HIV education significantly predicts the number of sex partners.）

### 📌 2. 愛滋病篩檢行為與性伴侶數量的關聯性 / Association of HIV Testing History
* **中文**: 青少年是否曾做過愛滋病篩檢，與其性伴侶數量是否存在顯著關聯？（探討高風險行為者是否具備較高的健康篩檢防護意識）
* **English**: Is there a significant association between a student's HIV testing history and their number of sex partners? (To explore whether higher-risk individuals exhibit greater health-seeking and screening consciousness.)
* **假設檢定 / Hypotheses**:
  * $H_0: \beta_2 = 0$ （篩檢經歷對性伴侶數量沒有顯著預測效果 / HIV testing history does not significantly predict the number of sex partners.）
  * $H_1: \beta_2 \neq 0$ （篩檢經歷對性伴侶數量具有顯著預測效果 / HIV testing history significantly predicts the number of sex partners.）

### 📌 3. 安全防護行為（保險套使用）與性伴侶數量的綜合關係 / Predictive Effect of Condom Use
* **中文**: 最近一次性行為中是否有使用保險套，是否能顯著預測青少年過去 3 個月內的總性伴侶數量？
* **English**: Does condom use during the last sexual intercourse significantly predict the total number of sex partners within the past 3 months?
* **假設檢定 / Hypotheses**:
  * $H_0: \beta_3 = 0$ （上次保險套使用對性伴侶數量沒有顯著預測效果 / Condom use does not significantly predict the number of sex partners.）
  * $H_1: \beta_3 \neq 0$ （上次保險套使用對性伴侶數量具有顯著預測效果 / Condom use significantly predicts the number of sex partners.）
