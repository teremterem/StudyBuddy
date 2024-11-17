import streamlit as st

# Set the page layout to wide
st.set_page_config(layout="wide")

# Create two columns: one for the text area and one for the preview
col1, col2 = st.columns(2)

with col1:
    st.header("Input")
    # Text area for user input
    text_input = st.text_area("Enter your Markdown text here:")

with col2:
    st.header("Preview")
    # Live preview of the Markdown content
    st.markdown(text_input)

# Submit button
if st.button("Submit"):
    st.write("Submitted content:")
    st.markdown(text_input)
