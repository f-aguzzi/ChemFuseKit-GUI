"""
# Data fusion

A graphical user interface for the data fusion module in `ChemFuseKit`.
"""

import streamlit as st
from chemfusekit.df import Table, DFSettings, DF
from io import BytesIO
import pandas as pd

st.title("ChemFuseKit data fusion module")

st.markdown(f"""
Use this web application to leverage the data fusion abilities of ChemFuseKit.

**Instructions:**
1. upload your table files
2. insert the settings for each table in the forms, and submit them one by one
3. select the fusion technique
4. click "Fuse tables"
5. download the resulting data
""")

tables = st.file_uploader(label="Upload your tables here", accept_multiple_files=True)

if "tabled_tables" not in st.session_state:
    st.session_state.tabled_tables = []

for table in tables:
    file = BytesIO(table.read())
    with st.form(f"Form for table {table}"):
        st.markdown(f"Import settings for: {table.name}")
        if table.name.endswith(".xlsx"):
            sheet_name = st.text_input("Sheet name: ")
        else:
            sheet_name = 'none'
        preprocessing = st.selectbox(
            "Preprocessing (SNV, Savitski-Golay, both or none)",
            ("snv", "savgol", "savgol+snv", "none"))
        feature_selection = st.selectbox(
            "Feature selection (PCA, PLSDA or none)",
            ("pca", "plsda", "none"))
        class_column = st.text_input("Class column: ")
        index_column = st.text_input("Index column: ")
        submitted = st.form_submit_button("Submit")

        if submitted:
            st.session_state.tabled_tables.append(Table(
                file_path=file,
                sheet_name=sheet_name if sheet_name != '' else 'Sheet1',
                preprocessing=preprocessing,
                feature_selection=feature_selection if feature_selection != 'none' else None,
                class_column=class_column if class_column != '' else 'Substance',
                # index_column=index_column
            ))

if len(tables) > 0:
    st.markdown(f"Imported {len(st.session_state.tabled_tables)} tables.")

if len(st.session_state.tabled_tables) > 0:
    fusion_type = st.selectbox(
            "Fusion technique: ",
            ("concat", "outer"))

    if st.button("Fuse data"):
        df = DF(DFSettings(output='none', method=fusion_type), st.session_state.tabled_tables)
        df.fuse()
        df.fused_data.x_train

        buffer = BytesIO()
        with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
            # Write each dataframe to a different worksheet.
            df.fused_data.x_train.to_excel(writer, sheet_name='Sheet1')

            # Close the Pandas Excel writer and output the Excel file to the buffer
            writer.close()

            st.download_button(
                label="Download fused data as Excel",
                data=buffer,
                file_name="fused_data.xlsx",
                mime="application/vnd.ms-excel"
            )
