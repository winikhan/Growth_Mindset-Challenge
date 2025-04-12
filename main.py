import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="File Converter & Cleaner", page_icon=":guardsman:", layout="wide")
st.title("File Converter & Cleaner🧹")
st.write("Upload Your CSV or Excel File to change the format of your files and clean the data within few clicks!🚀")

files_uploader = st.file_uploader(
    "Upload your CSV or Excel files, one or multiple files at once.",
    type=["csv", "xlsx"],
    accept_multiple_files=True
)

if files_uploader:
    for file in files_uploader:
        ext = file.name.split(".")[-1]
        df = pd.read_csv(file) if ext == "csv" else pd.read_excel(file)
        st.subheader(f"🔍Preview {file.name}")
        st.dataframe(df.head(5))

        # Fill Missing Values
        if st.checkbox(f"Fill The Missing Values - {file.name}"):
            df.fillna(df.select_dtypes(include=["number"]).mean(), inplace=True)
            st.success("Missing values have been filled successfully🙌.")
            st.dataframe(df.head())

            selected_columns = st.multiselect(
                f"Select columns to convert to CSV, {file.name}",
                df.columns,
                default=df.columns
            )
            df = df[selected_columns]
            st.dataframe(df.head())

        # Show Chart
        if st.checkbox(f"Show chart - {file.name}") and not df.select_dtypes(include=["number"]).empty:
            st.subheader(f"📊Chart - {file.name}")
            st.bar_chart(df.select_dtypes(include=["number"]).iloc[:, 0:2])

            # File Conversion
            select_type = st.radio(
                f"Convert {file.name} to:",
                ["CSV", "Excel"],
                key=f"{file.name}_convert"
            )

            output = BytesIO()
            if select_type == "CSV":
                df.to_csv(output, index=False)
                mime = "text/csv"
                new_file = file.name.replace(ext, "csv")
            else:
                df.to_excel(output, index=False, engine='openpyxl')  # Ensure openpyxl is installed
                output.seek(0)  # Reset the stream position to the beginning
                mime = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                new_file = file.name.replace(ext, "xlsx")

            st.download_button(
                label=f"⬇️Download your file {file.name} as {select_type}",
                data=output.getvalue(),
                file_name=new_file,
                mime=mime
            )
            st.success(f"File {new_file} has been downloaded successfully!🚀")