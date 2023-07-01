import pandas as pd
import streamlit as st
import requests
from PIL import Image
from io import BytesIO

# Load the CSV file
data = pd.read_csv('disagree_to_code.csv')

# Checkbox to control whether only empty label rows are displayed
only_empty = st.checkbox('Show only rows where label is empty', value=True)

# Find the first row where 'label' is empty 
empty_rows = iter(data[data['label'].isna()].index)
start_row = next(empty_rows)

# If only empty rows should be displayed and checkbox is False, start from the beginning
if not only_empty:
    start_row = 0

# Set the row to start from
row = st.number_input('Row number', min_value=0, max_value=len(data)-1, value=start_row, step=1)

# Get the data for this row
entry = data.iloc[row]

# Display status
if pd.isnull(data.loc[row, 'label']):
    st.markdown("<h2 style='color: red'>INCOMPLETE</h2>", unsafe_allow_html=True)
else:
    st.markdown("<h2 style='color: mediumseagreen'>COMPLETE</h2>", unsafe_allow_html=True)

# Display bioguide
st.write(f"Bioguide: {entry['bioguide']}")

# Get the input from the user
label = st.radio(
    "Is this the same person?",
    ('Yes', 'No', "Don't know")
)

# Button for saving the label and moving to the next row
if st.button('Enter'):
    # Assign the label to the row
    data.loc[row, 'label'] = label

    # Save the CSV file
    data.to_csv('disagree_to_code.csv', index=False)
    
    # If only_empty is true, find the next row where 'label' is empty
    if only_empty:
        row = next(empty_rows, 'No more empty rows')
        if row == 'No more empty rows':
            st.write('No more rows with empty labels.')
        else:
            st.write(f'Next row with an empty label: {row+1}')

# Get the images
image1 = Image.open(BytesIO(requests.get(entry['portrait_url']).content))
image2 = Image.open(BytesIO(requests.get(entry['image_url']).content))

# Display the images
col1, col2 = st.columns(2)
with col1:
    st.image(image1, use_column_width=True)
with col2:
    st.image(image2, use_column_width=True)

st.write(f"You are at row {row+1} of {len(data)}")

# Download

def convert_df(df):
   return df.to_csv(index=False).encode('utf-8')


csv = convert_df(data)

st.download_button(
   "Press to Download",
   csv,
   "file.csv",
   "text/csv",
   key='download-csv'
)

