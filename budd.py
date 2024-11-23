from pathlib import Path

import streamlit as st

from study_buddy import text_to_mp3


PAGE_TITLE = "Text-to-Speech"


st.set_page_config(page_title=PAGE_TITLE, layout="wide")

st.header(PAGE_TITLE)

# Wrap the text area and button in a form
with st.form("text_to_speech_form", border=False):
    text_input = st.text_area(
        "Enter text here:", placeholder="Enter text here", label_visibility="collapsed", height=300
    )
    submit_button = st.form_submit_button("Read Aloud")  # Submit button for the form

if submit_button and text_input:
    # TODO what about html injections ?
    st.html(f"<pre style='white-space: pre-wrap;'>{text_input}</pre>")

    mp3_file = Path("temp.mp3")
    text_to_mp3(text_input, mp3_file)
    st.audio(mp3_file.read_bytes(), format="audio/mp3", autoplay=True)
