import streamlit as st
from supabase import create_client
import pandas as pd

st.set_page_config(page_title="NHOP Data Explorer", layout="wide")

# Streamlit UI
st.title("📊 NHOP Data Explorer")

# Connect to Supabase
url = st.secrets["supabase_url"]
key = st.secrets["supabase_key"]
supabase = create_client(url, key)

# List your uploaded table names here manually
tables = ["nhop_ytd_sales"]
table = "nhop_ytd_sales"

# Fetch data from Supabase
data = supabase.table(table).select("*").order("Posting Date", desc=True).limit(1000).execute()
df = pd.DataFrame(data.data)

# Define specific columns you want to filter on
filter_columns = ["Month-YY"]

# Apply filters
filtered_df = df.copy()
for col in filter_columns:
    if col in df.columns:
        options = df[col].dropna().unique()
        selected = st.multiselect(f"Filter by {col}", options, default=options)
        filtered_df = filtered_df[filtered_df[col].isin(selected)]

# Show filtered data
st.dataframe(filtered_df, use_container_width=True)

# # Download option
    # csv = df.to_csv(index=False).encode("utf-8")
    # st.download_button("Download CSV")
