# 📊 AI-Powered Data Analyzer

An interactive Streamlit web app that allows users to **upload CSV files**, explore **summary insights**, view an interactive **dashboard**, and finally **export the summary to PDF**.

---
#### Click here - 👉 [AI-Powered Data Analyzer](https://ai-powered-data-analyzer-4vmbeigc64kmmeuj6urgcw.streamlit.app/)
---
## 🛠️ Libraries Used
- Streamlit
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Altair

---

## ⚙️ Approach & Project Structure

### `Home.py`
- Defines the **page configuration** and **title**.  
- Provides a **file uploader** for CSV files.  
- Displays **summary insights** of the uploaded dataset.  
- Includes an **Export to PDF** button.

---

### `utils.py`
A utility module where all reusable functions are defined using Pandas and other libraries:  

1. **`clean_data(df)`** → Handles null values and duplicates.  
2. **`handle_datetime(df)`** → Converts date/time columns to appropriate datatypes.  
3. **`handle_outliers(df)`** → Removes outliers using the Winsorization method.  
4. **`separate_cols(df)`** → Automatically detects and separates columns into:
   - Date columns  
   - Numeric columns  
   - Categorical columns  
   - Time columns  
5. **`compute_kpis(df, col)`** → Returns KPIs (Sum / Count) for a selected column.  
6. **`export_summary_to_pdf(df)`** → Exports the dataset summary into a PDF file.  

---

### `pages/Visualization.py`
- Imports all required libraries and utility functions.  
- Displays a **warning** if no dataset is uploaded in `Home.py`.  
- Once data is available, applies utility functions from `utils.py`.  
- Generates **KPIs** for selected numeric columns.  
- Creates interactive **charts** and dashboard visualizations.  

---


