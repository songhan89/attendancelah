import streamlit as st
import pytesseract
from PIL import Image
import pandas as pd

# Function to perform OCR and extract text from an image
def extract_text_from_image(image):
    text = pytesseract.image_to_string(image)
    return text

# Function to process the extracted text and create a pandas dataframe
def process_text_to_dataframe(text):
    # Split the text by lines and remove any empty lines
    lines = text.split('\n')
    names = [line.strip() for line in lines if line.strip()]

    # Create a pandas dataframe from the names list
    df = pd.DataFrame(names, columns=['Name'])

    # Sort the dataframe alphabetically by name
    df = df.sort_values(by='Name').reset_index(drop=True)

    return df

# Streamlit app title
st.title("OCR Attendance Helper")

# Add a small introduction
st.write("This app helps extract text from an image (e.g., attendance list) and process it to create a list of attendees.")
# Build by
st.write("Built by [Wong Songhan](https://github.com/songhan89)")

# Upload image
uploaded_image = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_image is not None:
    # Display the uploaded image
    image = Image.open(uploaded_image)
    st.image(image, caption='Uploaded Image', use_column_width=True)
    
    # Extract text from the image
    extracted_text = extract_text_from_image(image)
    
    # Process the extracted text and create a dataframe
    name_df = process_text_to_dataframe(extracted_text)
    
    # Count the total number of attendees
    total_attendees = name_df.shape[0]
    
    # Additional processing
    name_df['Skype'] = name_df['Name']
    name_df['Name'] = name_df['Name'].str.replace(""" (NEA)""", "").str.title()
    name_df = name_df.drop_duplicates(subset=['Name'], keep='last')

    # Display the dataframe and total number of attendees
    st.write(f'Total number of attendees: {total_attendees}')

    # Display the processed dataframe
    st.write("Processed DataFrame:")
    st.dataframe(name_df)
    
    # Export the dataframe to a CSV file if needed
    csv = name_df.to_csv(index=False)
    st.download_button(label="Download CSV", data=csv, file_name='attendees_list.csv', mime='text/csv')

# To run the app, use the command: streamlit run your_script_name.py

