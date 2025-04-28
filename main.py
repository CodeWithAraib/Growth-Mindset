import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="📁 File Converter & Cleaner",layout="wide")
st.title("📁 File Converter & Cleaner")
st.write("Upload a CSV file to convert it to Excel format and clean the data.🚀")

uploaded_file = st.file_uploader("Upload CSV and Excel files", type=["csv", "xlsx"], accept_multiple_files=True)

if uploaded_file:
    for file in uploaded_file:
       exe = file.name.split(".")[-1]
       df = pd.read_csv(file) if exe == ('csv') else pd.read_excel(file)

    st.write(f"🔎{file.name} - Preview")
    st.dataframe(df.head())
    
    if st.checkbox(f"File missing values for {file.name}"):
        df.fillna(df.select_dtypes(include=['number']).mean(), inplace=True)
        st.write("Missing values filled has successfully.")
        st.dataframe(df.head())

    select_columns = st.multiselect(
    f"Select columns to keep {file.name}",  # Added space for better formatting
    df.columns, 
    default=df.columns  # ← Correct spelling
)
    df = df[select_columns]
    st.write("Selected columns:")
    st.dataframe(df.head())

    if st.checkbox(f"📊 Show Chart - {file.name}") and not df.select_dtypes(include="number").empty:
        st.write("📊 Chart")
    st.bar_chart(df.select_dtypes(include="number").iloc[:, :5])

    format_choice = st.radio(f"Select file to convert {file.name} to:", ["Excel", "CSV"], key=file.name)

    if st.button(f"📩Download {file.name} to {format_choice}"):
        output = BytesIO()
        if format_choice == "CVS":
            df.to_excel(output, index=False)
            mime = "text/csv"
            new_name = file.name.replace(".xlsx", ".csv")
        else:
            df.to_excel(output, index=False)
            mime = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            new_name = file.name.replace(".csv", ".xlsx")
            output.seek(0)
        st.download_button("📩Download File", data=output, file_name=new_name, mime=mime) 
        st.success(f"Processed file {new_name} downloaded successfully!")

