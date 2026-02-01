import streamlit as st
import pytz

from streamlit_gsheets import GSheetsConnection
import datetime
import pandas as pd

# -----------------------------
# Page config (must be first)
# -----------------------------
st.set_page_config(
    page_title="Push-up Tracker",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# -----------------------------
# Google Sheets connection
# -----------------------------
conn = st.connection("gsheets", type=GSheetsConnection)

# -----------------------------
# Cached read (FAST)
# -----------------------------
@st.cache_data(ttl=30)
def load_data():
    return conn.read(worksheet="Sheet1")

# -----------------------------
# UI
# -----------------------------
st.title("Push-ups 2026")
st.subheader("100 Pushups. 365 Days. One Winner.")

names = ["Vail", "Marcus", "Tayte"]
user = st.selectbox("Who is logging today?", names)

TORONTO_TZ = pytz.timezone("America/Toronto")
today = datetime.datetime.now(TORONTO_TZ).strftime("%Y-%m-%d")
existing_data = load_data()

# Normalize data
existing_data["Date"] = (
    pd.to_datetime(existing_data["Date"], errors="coerce")
    .dt.strftime("%Y-%m-%d")
)

existing_data["Name"] = existing_data["Name"].astype(str).str.strip()


# -----------------------------
# Check if already logged
# -----------------------------
already_logged = (
    (existing_data["Date"] == today) &
    (existing_data["Name"] == user)
).any()


if already_logged:
    st.warning(f"Nice try, {user}, you've already logged today.")
    st.stop()  # 🔥 hard stop — prevents writes

# -----------------------------
# Submit
# -----------------------------
if st.button("Submit 100 Pushups", disabled=already_logged):
    new_row = pd.DataFrame([{
        "Date": today,
        "Name": user,
        "Completed": 1
    }])

    updated_df = pd.concat([existing_data, new_row], ignore_index=True)

    conn.update(worksheet="Sheet1", data=updated_df)

    st.cache_data.clear()  # force refresh for next user
    st.balloons()
    st.success("Entry locked in. See you tomorrow 🏆")

# -----------------------------
# Footer
# -----------------------------
st.divider()
st.caption("Leaderboard is hidden. Final reveal: January 26, 2027.")

