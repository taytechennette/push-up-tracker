import streamlit as st
from streamlit_gsheets import GSheetsConnection

conn = st.connection("gsheets", type=GSheetsConnection)

df = conn.read(
    spreadsheet="https://docs.google.com/spreadsheets/d/1IATA3PigWIDeTLl_iG-cxTq-pRXOwM-a7HYIm5VRbY0",
    worksheet="Sheet1"
)

print(df.head())
