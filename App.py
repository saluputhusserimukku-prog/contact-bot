import streamlit as st
import pandas as pd

st.set_page_config(page_title="Contact Bot", layout="centered")

# -------- Allowed Users (phone login) --------
ALLOWED = {"9744244711", "9496240520"}  # change

if "ok" not in st.session_state:
    st.session_state.ok = False

if not st.session_state.ok:
    p = st.text_input("Enter authorized mobile number")
    if st.button("Login"):
        if p in ALLOWED:
            st.session_state.ok = True
            st.rerun()
        else:
            st.error("Not allowed")
    st.stop()

# -------- Load Excel --------
@st.cache_data
def load():
    df = pd.read_excel("contacts.xlsx")
    df.columns = df.columns.str.strip()
    return df

df = load()

def get_mobile(r):
    for c in ["Mobile","Phone","Phone No"]:
        if c in df.columns:
            return r[c]
    return "NA"

st.title("📱 Contact Search Bot")

mode = st.radio(
    "Search Mode",
    ["By Name","By Unit + Designation"],
    horizontal=True
)

if mode == "By Name":
    name = st.selectbox("Select Name", sorted(df["Name"].unique()))
    if st.button("Search"):
        r = df[df["Name"] == name].iloc[0]
        st.success(f"""
Name: {r['Name']}
Unit: {r['Unit']}
Designation: {r['Designation']}
Mobile: {get_mobile(r)}
""")

else:
    unit = st.selectbox("Unit", sorted(df["Unit"].unique()))
    sub = df[df["Unit"] == unit]
    des = st.selectbox("Designation", sorted(sub["Designation"].unique()))
    if st.button("Search"):
        r = sub[sub["Designation"] == des].iloc[0]
        st.success(f"""
Name: {r['Name']}
Unit: {r['Unit']}
Designation: {r['Designation']}
Mobile: {get_mobile(r)}
""")
