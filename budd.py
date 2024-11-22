from pathlib import Path

import streamlit as st

from study_buddy import text_to_mp3

st.set_page_config(layout="wide")

(col1,) = st.columns(1)

with col1:
    st.header("OpenAI Text-to-Speech")
    text_input = st.text_area("Enter text here:")

if st.button("Read aloud") and text_input:
    # TODO what about html injections ?
    st.html(f"<pre style='white-space: pre-wrap;'>{text_input}</pre>")

    mp3_file = Path("temp.mp3")
    text_to_mp3(text_input, mp3_file)
    st.audio(mp3_file.read_bytes(), format="audio/mp3", autoplay=True)
