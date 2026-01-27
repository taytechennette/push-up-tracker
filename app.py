import streamlit as st
from streamlit_gsheets import GSheetsConnection
import datetime
import pandas as pd

# Connect to the Sheet
conn = st.connection("gsheets", type=GSheetsConnection)

st.title("Push-ups 2026")
st.subheader("100 Pushups. 365 Days. One Winner.")

# User Selection
names = ["Vail", "Marcus", "Tayte"] # Replace with your real names
user = st.selectbox("Who is logging today?", names)

if st.button("Submit 100 Pushups"):
    # 1. Fetch existing data to prevent double-logging
    existing_data = conn.read(worksheet="Sheet1", usecols=[0,1])
    today = str(datetime.date.today())
    
    # Check if this user already logged today
    already_logged = existing_data[(existing_data['Date'] == today) & (existing_data['Name'] == user)]
    
    if not already_logged.empty:
        st.error(f"Nice try, {user}. You already logged your reps for today!")
    else:
        # 2. Add new row
        new_row = pd.DataFrame([{"Date": today, "Name": user, "Completed": 1}])
        updated_df = pd.concat([existing_data, new_row], ignore_index=True)
        
        # 3. Update the Sheet
        conn.update(worksheet="Sheet1", data=updated_df)
        st.balloons()
        st.success("Entry locked in. See you tomorrow.")

st.divider()
st.caption("Leaderboard is hidden. Final reveal: January 26, 2027.")