import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module='pandas')
import utilis as ut
import altair as alt
import seaborn as sns

# Setting Page Configuration

st.set_page_config(layout='wide')

st.title('Dashboard')

# Giving Warning when dataset is not uploaded

df = st.session_state.get('df', None)

if df is None:
    st.warning('⚠️ No Dataset found in session. Please go back to the Home page and upload your file.') 
    st.stop()

# Analyzing once dataset is uploaded

# -> Cleaning data - handling nills, datetime columns, separting cols

df = ut.clean_data(df)
df = ut.handle_datetime(df)
# df = ut.handle_outliers(df)

cat_cols,num_cols,date_cols,time_cols = ut.separate_cols(df)

# -> Generating KPI's

k1, k2, k3, k4 = st.columns(4)

k1.metric("Rows", f"{len(df):,}")
k2.metric("Columns", df.shape[1])
k3.metric("Missing %", f"{df.isna().mean().mean()*100:.2f}")
k4.metric("Numeric / Categorical", f"{len(num_cols)} / {len(cat_cols)}")

st.markdown("""<style>[data-testid="stMetric"] { background:#f8fafc; padding:12px; border-radius:12px; }</style>""", unsafe_allow_html=True)

st.divider()

# -> Giving Sidebar controls

with st.sidebar:
    st.header('Chart Controls')

    # LINE
    line_date = st.selectbox("Line: Date column",date_cols + ["(none)"])
    line_y = st.selectbox("Line: Numeric Y", num_cols + ["(none)"])

    # BAR
    bar_cat = st.selectbox("Bar: Category", cat_cols + ["(none)"])
    bar_metric = st.radio("Bar: Metric", ["Count", "Sum"], horizontal=True)
    bar_value = st.selectbox("Bar: Sum of (if Sum)", num_cols + ["(none)"])

    # HEATMAP
    heat_cols = st.multiselect("Heatmap: numeric columns", num_cols, default=num_cols[:6])

    # PIE
    pie_cat = st.selectbox("Pie: Category", cat_cols +  ["(none)"])


# Genearatin Charts (2*2 grid)

c1,c2 = st.columns(2)

with c1:
    st.subheader("Line Chart")
    if line_date != "(none)" and line_y != "(none)":
        tmp = df[[line_date, line_y]].dropna()
        ts = tmp.groupby(line_date)[line_y].mean().reset_index()
        chart = (alt.Chart(ts).mark_line(point=True).encode(
          x = alt.X(line_date,type='temporal',title=line_date),
          y = alt.Y(line_y,type='quantitative',title=f'{line_y} (mean)')
        ))
        st.altair_chart(chart, use_container_width=True)
    else:
        st.info("Select date and numeric column")

with c2:
    st.subheader("Bar Chart")
    if bar_cat != "(none)":
        if bar_metric == "Count":
            tmp = df[bar_cat].value_counts().reset_index()
            tmp.columns = [bar_cat, "Count"]
            chart = alt.Chart(tmp).mark_bar().encode(x=bar_cat, y="Count")
            st.altair_chart(chart, use_container_width=True)
        elif bar_metric == "Sum" and bar_value != "(none)":
            tmp = df.groupby(bar_cat)[bar_value].sum().reset_index()
            chart = alt.Chart(tmp).mark_bar().encode(x=bar_cat, y=bar_value)
            st.altair_chart(chart, use_container_width=True)
        else:
            st.info("Pick a numeric column for Sum")
    else:
        st.info("Select category column")
        

c3,c4 = st.columns(2)

with c3:
    st.subheader("Heatmap")
    if heat_cols:
        corr = df[heat_cols].corr()
        fig, ax = plt.subplots()
        sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax)
        st.pyplot(fig)
    else:
        st.info("Pick numeric columns for heatmap")

with c4:
    st.subheader("Pie Chart")
    if pie_cat != "(none)":
        tmp = df[pie_cat].value_counts().reset_index()
        tmp.columns = [pie_cat, "count"]
        fig, ax = plt.subplots()
        ax.pie(tmp["count"], labels=tmp[pie_cat], autopct="%1.1f%%", startangle=90)
        st.pyplot(fig)
    else:
        st.info("Pick category column")


st.divider()


# -> Genrating Stastical summary

st.subheader("Statistical Summary")
st.dataframe(df.describe(include='all').T)

st.subheader('Get Preview of Data')
st.dataframe(df.sample(10))
