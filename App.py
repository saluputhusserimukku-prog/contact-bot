import streamlit as st
import pandas as pd

st.set_page_config(page_title="Secure Contact Bot", layout="centered")

# --------- ALLOWED PHONE NUMBERS ---------
ALLOWED_NUMBERS = {
    "9744244711",
    "9496240520",
}   # ← replace with real allowed numbers


# --------- PHONE LOGIN ---------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:

    st.title("📱 Secure Contact Bot Login")

    phone = st.text_input("Enter your registered mobile number")

    if st.button("Verify"):
        phone = phone.strip()

        if phone in ALLOWED_NUMBERS:
            st.session_state.logged_in = True
            st.session_state.user_phone = phone
            st.success("Access granted")
            st.rerun()
        else:
            st.error("❌ Not authorized")

    st.stop()


# -------- LOAD DATA --------
@st.cache_data
def load_data():
    df = pd.read_excel("contacts.xlsx")
    df.columns = df.columns.str.strip()
    return df

df = load_data()


# -------- MOBILE COLUMN SAFE --------
def get_mobile(row):
    for col in ["Mobile", "Phone", "Phone No", "Mobile No"]:
        if col in df.columns:
            return row[col]
    return "Not Available"


# -------- APP --------
st.title("📞 Officer Contact Lookup")

mode = st.radio(
    "Search Mode",
    ["Search by Name", "Search by Unit + Designation"],
    horizontal=True
)

# -------- NAME DROPDOWN --------
if mode == "Search by Name":

    name = st.selectbox(
        "Select Officer",
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


# -------- UNIT + DESIGNATION --------
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


st.caption("Authorized Mobile Access Only")
