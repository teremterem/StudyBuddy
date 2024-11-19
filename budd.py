import streamlit as st

from study_buddy import text_to_mp3

# Set the page layout to wide
st.set_page_config(layout="wide")

col1, = st.columns(1)

with col1:
    st.header("Input")
    # Text area for user input
    text_input = st.text_area("Enter your Markdown text here:")

# Submit button
if st.button("Submit"):
    if text_input:
        text_to_mp3(text_input, "temp.mp3")

    st.write("Submitted content:")
    st.markdown(text_input)
