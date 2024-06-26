"""
# Data fusion

A graphical user interface for the data fusion module in `ChemFuseKit`.
"""

import streamlit as st
from chemfusekit.df import Table

st.title("ChemFuseKit data fusion module")

st.markdown(f"""
Use this web application to leverage the data fusion abilities of ChemFuseKit.
""")

tables = st.file_uploader(label="Upload your tables here", accept_multiple_files=True)

tabled_tables = []
for table in tables:
    with st.form(f"Form for table {table}"):
        st.markdown(f"Import settings for: {table.name}")
        if table.name.endswith(".xlsx"):
            sheet_name = st.text_input("Sheet name: ")
        else:
            sheet_name = 'none'
        preprocessing = st.selectbox(
            "Preprocessing",
            ("snv", "savgol", "savgol+snv", "none"),)
        feature_selection = st.selectbox(
            "Feature selection",
            ("pca", "plsda", "none"))
        class_column = st.text_input("Class column: ")
        index_column = st.text_input("Index column: ")
        submitted = st.form_submit_button("Submit")
        if submitted:
            tabled_tables.append(Table(
                file_path=table.file_id,
                sheet_name=sheet_name,
                preprocessing=preprocessing,
                feature_selection=feature_selection,
                class_column=class_column,
                index_column=index_column
            ))
    
