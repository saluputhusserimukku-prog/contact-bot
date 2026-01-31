import streamlit as st
import pandas as pd

st.title("📘 Officer Contact Chatbot")

# Load Excel
df = pd.read_excel("contacts.xlsx")

# Clean search columns
df["Name_clean"] = df["Name"].str.lower().str.strip()
df["Designation_clean"] = df["Designation"].str.lower().str.strip()
df["Unit_clean"] = df["Unit"].str.lower().str.strip()

query = st.text_input("Enter Name OR 'Designation, Unit'")

if query:

    q = query.lower().strip()

    # ---- designation + unit mode ----
    if "," in q:
        desig, unit = [x.strip() for x in q.split(",", 1)]

        result = df[
            (df["Designation_clean"] == desig) &
            (df["Unit_clean"] == unit)
        ]

        if result.empty:
            st.error("No matching officers found.")
        else:
            for _, r in result.iterrows():
                st.success(
                    f"""
Name: {r['Name']}
Mobile: {r['Mobile']}
"""
                )

    # ---- name search mode ----
    else:
        result = df[df["Name_clean"].str.contains(q, na=False)]

        if result.empty:
            st.error("No officer found.")
        else:
            for _, r in result.iterrows():
                st.success(
                    f"""
Name: {r['Name']}
Designation: {r['Designation']}
Unit: {r['Unit']}
Mobile: {r['Mobile']}
"""
                )
