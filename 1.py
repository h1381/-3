import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from google.oauth2.service_account import Credentials

sheet_url = "https://docs.google.com/spreadsheets/d/1y-75Hy8CQbPL8WeAK9jsfkiWJbKk4cBcaTax1S3JuA0/edit?gid=0#gid=0"
csv_export_url = sheet_url.replace('/edit?usp=sharing', '/gviz/tq?tqx=out:csv')



def get_data(url):
    return pd.read_csv(url)

def add_data_to_sheet(data):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = Credentials.from_service_account_file("YOUR_SERVICE_ACCOUNT_JSON_FILE.json", scopes=scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_url(sheet_url).sheet1
    sheet.append_row(data)

def update_data_in_sheet(row_index, data):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = Credentials.from_service_account_file("YOUR_SERVICE_ACCOUNT_JSON_FILE.json", scopes=scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_url(sheet_url).sheet1
    for col, value in enumerate(data, start=1):
        sheet.update_cell(row_index, col, value)
def delete_data_in_sheet(row_index):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = Credentials.from_service_account_file("YOUR_SERVICE_ACCOUNT_JSON_FILE.json", scopes=scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_url(sheet_url).sheet1
    sheet.delete_rows(row_index)

st.set_page_config(
    page_title=" Google Sheet my",
    layout="wide",
)
st.markdown("""
    <style>
        .main {
            background-color: ##C2E7D9;
            color: #black;
        }
        h1, h2 {
            color: #fffff;
        }
      
        .stTextInput input {
            border: 2px solid  #0D0221;
            padding: 12px;
            border-radius: 9px;
            background-color:#A6CFD5;
            color: #black;
        }
        .stDataFrame {
            background-color: #fffff;
            color: black;
        }


  .stButton button {
            background-color: #D6FAFF;
            color: #black;
        }

        .css-1cpxqw2 a {
            color: #0F084B; }
    </style>
""", unsafe_allow_html=True)
st.title("📈 Google Sheet 📉")
st.header("⬇ My Data ⬇")
data = get_data(csv_export_url)
st.dataframe(data, width=1000, height=400)

st.header("  New Data")
with st.form(key='add_data_form'):
    new_data = {}
    columns = data.columns
    for column in columns:
        new_data[column] = st.text_input(f"Enter {column}", "")

    submit_button = st.form_submit_button(label='Add Data')

if submit_button:
    if any(new_data.values()):
        add_data_to_sheet(list(new_data.values()))
        st.success("Data added successfully!")
    else:
        st.error("Please fill in at least one field.")
data = get_data(csv_export_url)
st.header("📄 Updated Data")
st.dataframe(data, width=1200, height=500)

st.header("✏️ Edit Data")
selected_row = st.number_input("Enter the row number to edit", min_value=1, max_value=len(data))
if selected_row:
    with st.form(key='edit_data_form'):
        row_data = data.iloc[selected_row-1].to_dict()
        new_data = {}
        for column, value in row_data.items():
            new_data[column] = st.text_input(f"Enter new {column}", value)

        update_button = st.form_submit_button(label='Update Data')

    if update_button:
        if any(new_data.values()):
            update_data_in_sheet(selected_row, list(new_data.values()))
            st.success("Data updated successfully!")
        else:
            st.error("Please fill in at least one field.")
    data = get_data(csv_export_url)
    st.dataframe(data, width=1000, height=400)

st.header(" Delete ")
delete_row = st.number_input("Enter the row number to delete", min_value=1, max_value=len(data))
delete_button = st.button(label='Delete')

if delete_button:
    delete_data_in_sheet(delete_row)
    st.success(" deleted successfully!")
    data = get_data(csv_export_url)
    st.dataframe(data, width=1000, height=400)
