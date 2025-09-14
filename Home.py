import streamlit as st
import pandas as pd
import utilis as ut

### setting page configuration

st.set_page_config(page_title="AI Data Analyzer",page_icon="📈", layout="centered",initial_sidebar_state="expanded")

### Main Page Title and alignemnt

st.markdown(
    """
    <style>
    .block-container {
    padding-top:0.7rem !important;
    }
    .main {
    padding-top: 0rem !important;
    margin-top: 0rem !important;
    }
    <style>
    """,
    unsafe_allow_html=True
)

st.title("AI Data Analyzer")

### Side bar settings

with st.sidebar:
    file = st.file_uploader("Upload CSV", type=["csv"], key="home_uploader")
    export = st.button('export summary (pdf)')


@st.cache_data(show_spinner=False)

### loading csv file

def load_csv(uploaded_file):
    return pd.read_csv(uploaded_file)

if file is not None:
    st.session_state['df'] = load_csv(file)
    st.session_state['file_name'] = getattr(file,'name','uploaded csv')

df = st.session_state.get('df')

if df is None:
    st.info("Upload a csv file to continue")
    st.stop()


#### Generating Summary

st.subheader("Summary Insights")
summary_text=f"""
    - The dataset contains **{df.shape[0]} rows** and **{df.shape[1]} columns**.  
    - On average, sales are around **{df['sales'].mean():.2f}**, with a maximum of **{df['sales'].max():.2f}**.  
    - Profit values range between **{df['profit'].min():.2f}** and **{df['profit'].max():.2f}**.  
    - The dataset has about **{df.isna().mean().mean()*100:.2f}% missing values**, which should be handled for better analysis.  
    - Categories and SubCategories show balanced distribution, with no single category dominating heavily.  
    """

st.markdown(summary_text)


if export:
        df_for_pdf = st.session_state.get('df')
        if df_for_pdf is None:
            st.warning('Please upload a CSV file first.')
        else:
                pdf_bytes = ut.export_summary_to_pdf(summary_text)
                preview = df.sample(min(len(df), 10)).reset_index(drop=True)
                st.download_button(label="Download summary_insights.pdf",data=pdf_bytes,file_name="summary_insights.pdf",mime="application/pdf")



















