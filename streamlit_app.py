# streamlit_app.py
import streamlit as st
import requests
import base64
import io
import pandas as pd
import plotly.express as px

API_BASE = "https://csv-ai-dashboard.onrender.com/"  # Flask backend

st.set_page_config(page_title="CSV AI Dashboard", layout="wide")
st.title("CSV AI Dashboard")

# Upload and send to backend
uploaded = st.file_uploader("Upload a CSV file", type=["csv"])
if uploaded:
    files = {"file": uploaded}
    resp = requests.post(f"{API_BASE}/upload", files=files)
    if resp.ok:
        st.success("File uploaded to backend.")
        columns = resp.json().get("columns", [])
        st.write("Columns:", columns)
    else:
        st.error(f"Upload failed: {resp.text}")

# Query box
query = st.text_input("Ask a question about the data (natural language)", value="Show me total sales per region.")
if st.button("Run Query"):
    if not query:
        st.warning("Please enter a query")
    else:
        payload = {"query": query}
        r = requests.post(f"{API_BASE}/ask", json=payload)
        if not r.ok:
            st.error(f"Request failed: {r.text}")
        else:
            data = r.json()
            st.subheader("Plan (AI)")
            st.json(data.get("plan"))

            st.subheader("Text")
            st.write(data.get("text"))

            st.subheader("Table")
            table = data.get("table")
            if table:
                try:
                    df = pd.DataFrame(table)
                    st.dataframe(df)
                except Exception:
                    st.write(table)

            st.subheader("Chart")
            chart = data.get("chart")
            if chart and chart.get("data"):
                cdata = chart["data"]
                # If we received base64, show as image
                if chart.get("base64"):
                    st.image(base64.b64decode(chart["base64"]), use_column_width=True)

                # Also render interactive Plotly from chart data (if available)
                if cdata.get("x") and cdata.get("y"):
                    cdf = pd.DataFrame({"x": cdata["x"], "y": cdata["y"]})
                    if cdata.get("type") == "bar":
                        fig = px.bar(cdf, x="x", y="y", labels={"x": cdata.get("x_label"), "y": cdata.get("y_label")})
                    elif cdata.get("type") == "line":
                        fig = px.line(cdf, x="x", y="y", labels={"x": cdata.get("x_label"), "y": cdata.get("y_label")})
                    elif cdata.get("type") == "pie":
                        fig = px.pie(cdf, values="y", names="x")
                    else:
                        fig = px.bar(cdf, x="x", y="y")
                    st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No chart generated for this query.")
