import streamlit as st
import pandas as pd

st.set_page_config(page_title="Secure Contact Bot", layout="centered")

# -------- SECURITY LOGIN --------
PASSWORD = "police@123"   # change this

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("🔐 Secure Contact Bot Login")
    pw = st.text_input("Enter Password", type="password")

    if st.button("Login"):
        if pw == PASSWORD:
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Wrong password")

    st.stop()

# -------- LOAD DATA --------
@st.cache_data
def load_data():
    df = pd.read_excel("contacts.xlsx")
    df.columns = df.columns.str.strip()

    df["name_clean"] = df["Name"].astype(str).str.strip()
    df["unit_clean"] = df["Unit"].astype(str).str.strip()
    df["designation_clean"] = df["Designation"].astype(str).str.strip()

    return df

df = load_data()

st.title("📱 Officer Contact Lookup")

# detect mobile column safely
def get_mobile(row):
    for col in ["Mobile", "Phone", "Phone No", "Mobile No"]:
        if col in df.columns:
            return row[col]
    return "Not Available"


# -------- SEARCH MODE --------
mode = st.radio(
    "Search Mode",
    ["Search by Name", "Search by Unit + Designation"],
    horizontal=True
)

# -------- NAME DROPDOWN --------
if mode == "Search by Name":

    name = st.selectbox(
        "Select Officer Name",
        sorted(df["Name"].unique())
    )

    if st.button("Get Details"):
        r = df[df["Name"] == name].iloc[0]

        st.success(f"""
Name: {r['Name']}
Unit: {r['Unit']}
Designation: {r['Designation']}
Mobile: {get_mobile(r)}
""")


# -------- UNIT + DESIGNATION DROPDOWNS --------
else:

    unit = st.selectbox(
        "Select Unit",
        sorted(df["Unit"].unique())
    )

    filtered = df[df["Unit"] == unit]

    desig = st.selectbox(
        "Select Designation",
        sorted(filtered["Designation"].unique())
    )

    if st.button("Get Details"):
        r = filtered[filtered["Designation"] == desig].iloc[0]

        st.success(f"""
Name: {r['Name']}
Unit: {r['Unit']}
Designation: {r['Designation']}
Mobile: {get_mobile(r)}
""")

# -------- LOGOUT --------
if st.button("Logout"):
    st.session_state.logged_in = False
    st.rerun()
