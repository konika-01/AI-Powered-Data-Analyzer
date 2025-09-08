import streamlit as st
import pandas as pd

st.set_page_config(page_title="AI-Powered Data Analyzer", layout="wide")
st.title("AI-Powered Data Analyzer")

st.write("Upload a CSV to get started 👇")
file = st.file_uploader("Choose a CSV file now or you will die", type=["csv"])

if file is not None:
    df = pd.read_csv(file)
    st.success(f"Loaded {len(df):,} rows × {len(df.columns)} columns")
    st.dataframe(df, use_container_width=True)

    st.subheader("Quick Summary")
    st.write(df.describe(include="all").T)

    st.subheader("Pick columns to visualize")
    num_cols = df.select_dtypes("number").columns.tolist()
    if num_cols:
        x = st.selectbox("X-axis (numeric)", num_cols, index=0)
        st.line_chart(df[x])
    else:
        st.info("No numeric columns found for quick chart.")
else:
    st.info("No file uploaded yet.")