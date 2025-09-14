import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import utilis as ut
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module='pandas')
import altair as alt
from io import BytesIO
from datetime import datetime
import reportlab as rt

# Function for cleanin data
def clean_data(df):
    nulls = df.isnull().sum().sum()
    if nulls > 0:
        df = df.dropna()
    dup_no = df.duplicated().sum()
    if dup_no > 0:
        df.drop_duplicates(inplace=True)
    return df

# Function for handling outliers

def handle_outliers(df):
    num_cols = df.dtypes[df.dtypes!=object].index
    # to remove cat cols
    cols = [i for i in num_cols if df[i].nunique() > 10]
    for i in cols:
        lower = df[i].quantile(0.05)
        upper = df[i].quantile(0.95)
        df[i] = np.where(df[i]<lower,lower,df[i])
        df[i] = np.where(df[i]>upper,upper,df[i])
    return df

# Function for handling datatime cols

def handle_datetime(df):
    num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    columns = df.columns.str.strip()

    date_cols = [i for i in columns if 'date'in i.lower() and i not in num_cols]
    for i in date_cols:
        df[i] = pd.to_datetime(df[i],errors='coerce')

    time_cols = [i for i in columns if 'time' in i.lower() and i not in num_cols]
    for i in time_cols:
        df[i] = pd.to_datetime(df[i],errors='coerce',format='%H:%M:%S').dt.time
    return df

# Function for separating cols

def separate_cols(df):
    cols = df.columns.tolist()
    date_cols = df.select_dtypes( include=[np.datetime64, "datetime64[ns]", "datetimetz"]).columns.tolist()
    num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    cat_cols = [c for c in cols if c not in date_cols and df[c].nunique(dropna=True) <= 10]
    time_cols = [c for c in df.columns if "time" in c.lower()]
    return cat_cols,num_cols,date_cols,time_cols

# Generating KPIs

def compute_kpis(df,col):
    return{
        'sum': round(df[col].sum(),2),
        'median': round(df[col].median(),2),
        'max': round(df[col].max(),2),
        'min':round(df[col].min(),2)
    }

    

def hist_df(series: pd.Series, bins: int = 30) -> pd.DataFrame:
    s = series.dropna().to_numpy()
    if s.size == 0:
        return pd.DataFrame({"bin": [], "count": []}).set_index("bin")
    counts, edges = np.histogram(s, bins=bins)
    centers = (edges[:-1] + edges[1:]) / 2.0
    return pd.DataFrame({"bin": centers, "count": counts}).set_index("bin")

# Generating Summary function

def export_summary_to_pdf(summary_text):
    buf = BytesIO()
    doc = rt.SimpleDocTemplate(buf, pagesize=A4)
    styles = rt.getSampleStyleSheet()
    story = []

    story.append(Paragraph("Summary Insights", styles["Title"]))
    story.append(Paragraph(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M')}", styles["Normal"]))
    story.append(Spacer(1, 12))

    # add the summary text (convert newlines to paragraphs)
    for line in summary_text.strip().split("\n"):
        if line.strip():
            story.append(Paragraph(line.strip(), styles["Normal"]))
            story.append(Spacer(1, 6))

    doc.build(story)
    pdf_bytes = buf.getvalue()
    buf.close()
    return pdf_bytes

