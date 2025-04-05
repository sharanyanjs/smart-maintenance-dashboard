import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="Smart Maintenance Dashboard", layout="wide")

# Title & sidebar
st.title("🤖 Smart Maintenance Dashboard")
st.sidebar.title("Filter Options")

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv("data/dataset.csv")
    return df

df = load_data()

# Select metric
metrics = [col for col in df.columns if "metric" in col]
selected_metric = st.sidebar.selectbox("Select a metric to analyze", metrics)

# Filter by device
devices = df["device"].unique()
selected_device = st.sidebar.selectbox("Select a robot/device", ["All"] + list(devices))

# Filter dataframe
if selected_device != "All":
    df = df[df["device"] == selected_device]

# Z-score anomaly detection
df["zscore"] = (df[selected_metric] - df[selected_metric].mean()) / df[selected_metric].std()
df["anomaly"] = df["zscore"].abs() > 2
anomalies = df[df["anomaly"]]

# Main dashboard
st.subheader(f"📊 Anomaly Detection for `{selected_metric}`")

col1, col2 = st.columns(2)

with col1:
    st.metric("Total Data Points", len(df))
with col2:
    st.metric("Anomalies Detected", len(anomalies))

# Chart
fig = px.line(df, x="date", y=selected_metric, title=f"{selected_metric} Over Time", markers=True)
fig.add_scatter(x=anomalies["date"], y=anomalies[selected_metric],
                mode='markers', name="Anomalies", marker=dict(color='red', size=10))
st.plotly_chart(fig, use_container_width=True)

# Table
st.write("### 🔍 Anomalies Table")
st.dataframe(anomalies[["date", "device", selected_metric, "zscore"]])
