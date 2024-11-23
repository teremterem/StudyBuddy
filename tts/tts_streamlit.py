from pathlib import Path

import streamlit as st

from study_buddy import text_to_mp3

STATE_DIR = Path("state")
STATE_DIR.mkdir(exist_ok=True)

INPUT_TXT_FILE = STATE_DIR / "tts_input.txt"
OUTPUT_TXT_FILE = STATE_DIR / "tts_output.txt"
OUTPUT_MP3_FILE = STATE_DIR / "tts_output.mp3"

PAGE_TITLE = "Text-to-Speech"
st.set_page_config(page_title=PAGE_TITLE, layout="wide")
st.header(PAGE_TITLE)

with st.form("text_to_speech_form", border=False):
    text_input = st.text_area(
        "Enter text here:", placeholder="Enter text here", label_visibility="collapsed", height=300
    )
    INPUT_TXT_FILE.write_text(text_input, encoding="utf-8")
    print(repr(text_input))
    submitted = st.form_submit_button("Read Aloud")

    if submitted and text_input:
        st.html(f'<pre style="white-space: pre-wrap;">{text_input}</pre>')
        text_to_mp3(text_input, OUTPUT_MP3_FILE)
        st.audio(OUTPUT_MP3_FILE.read_bytes(), format="audio/mp3", autoplay=True)
