#!/usr/bin/env python
# coding: utf-8

# Running Toto prediction in Streamlit
# 
# Note: This code is not LSTM Model. It is Frequency-based predictor

# In[ ]:


# =======================================
# Toto Frequency-Based Prediction Dashboard
# Streamlit – Dev-Friendly Version
# =======================================

import pandas as pd
import numpy as np
import streamlit as st

# ---------------------------------------
# Google Sheet CSV Link (live data)
# ---------------------------------------
CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSqweBAM05Ab1y9aT4xQWn4cYog2vqAkvpRQL_PmUnU-vw38sQp0YTAs-VvNwkoz31kM_1kPgj4MShj/pub?gid=0&single=true&output=csv"

# ---------------------------------------
# Load data (no caching to see updates instantly)
# ---------------------------------------
def load_data():
    try:
        return pd.read_csv(CSV_URL)
    except Exception as e:
        st.error(f"Failed to load data: {e}")
        return pd.DataFrame()

df_raw = load_data()

# ---------------------------------------
# Streamlit UI
# ---------------------------------------
st.title("Toto Frequency-Based Predictor (Dev Mode)")
st.subheader("Latest 5 Rows from Google Sheet")
st.dataframe(df_raw.head())

# ---------------------------------------
# Parse the winning numbers
# ---------------------------------------
data = []
for _, row in df_raw.iterrows():
    try:
        winning_numbers = [int(x.strip().replace('"','')) for x in row['Winning No'].split(',')]
        additional_no = int(row['Additional No'])
        data.append(winning_numbers + [additional_no])
    except:
        continue

columns = ["n1","n2","n3","n4","n5","n6","add"]
df = pd.DataFrame(data, columns=columns)
df = df.iloc[::-1].reset_index(drop=True)  # chronological order

st.subheader("Latest 10 Draws (Chronological)")
st.dataframe(df.tail(10))

# ---------------------------------------
# Frequency Count
# ---------------------------------------
all_numbers = df[["n1","n2","n3","n4","n5","n6"]].values.flatten()
unique, counts = np.unique(all_numbers, return_counts=True)
freq_dict = dict(zip(unique, counts))

# Additional number frequency
unique_add, cnt_add = np.unique(df["add"], return_counts=True)
freq_add = dict(zip(unique_add, cnt_add))

st.subheader("Number Frequency Table")
freq_df = pd.DataFrame({"Number": unique, "Frequency": counts}).sort_values("Frequency", ascending=False)
st.dataframe(freq_df)

# ---------------------------------------
# Weighted Random Pick Function
# ---------------------------------------
def weighted_random_pick(freq_dictionary, k):
    num_pool = list(freq_dictionary.keys())
    weight_pool = list(freq_dictionary.values())
    picks = []

    for _ in range(k):
        pick = np.random.choice(num_pool, p=np.array(weight_pool)/sum(weight_pool))
        picks.append(int(pick))
        # Remove picked to avoid duplicates
        idx = num_pool.index(pick)
        num_pool.pop(idx)
        weight_pool.pop(idx)

    return sorted(picks)

# ---------------------------------------
# Prediction Button
# ---------------------------------------
if st.button("Generate Prediction"):
    main_nums = weighted_random_pick(freq_dict, k=6)
    add_num = weighted_random_pick(freq_add, k=1)[0]
    st.success(f"Predicted Numbers: {main_nums} + Add: {add_num}")


# In[ ]:


# !streamlit run toto_prediction_dashboard_v4.py 

