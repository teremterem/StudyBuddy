from pathlib import Path

import streamlit as st
from st_btn_group import st_btn_group

from study_buddy import text_to_mp3


STATE_DIR = Path("state")
STATE_DIR.mkdir(exist_ok=True)

INPUT_TXT_FILE = STATE_DIR / "tts_input.txt"
if not INPUT_TXT_FILE.exists():
    INPUT_TXT_FILE.touch()  # in case the user wants to use a different editor to enter text

OUTPUT_TXT_FILE = STATE_DIR / "tts_output.txt"
OUTPUT_MP3_FILE = STATE_DIR / "tts_output.mp3"

PAGE_TITLE = "Text-to-Speech"
st.set_page_config(page_title=PAGE_TITLE, layout="wide")
st.header(PAGE_TITLE)

if INPUT_TXT_FILE.exists():
    input_text = INPUT_TXT_FILE.read_text(encoding="utf-8")
else:
    input_text = ""

if OUTPUT_TXT_FILE.exists():
    output_text = OUTPUT_TXT_FILE.read_text(encoding="utf-8")
else:
    output_text = ""

blank_input = not input_text.strip()
updated_input = not blank_input and input_text != output_text
edit_mode = st.session_state.get("edit_mode", False)
update_audio = updated_input or not OUTPUT_MP3_FILE.exists()

print()
print(f"blank_input: {blank_input}")
print(f"updated_input: {updated_input}")
print(f"edit_mode: {edit_mode}")
print(f"update_audio: {update_audio}")

if updated_input:
    OUTPUT_TXT_FILE.write_text(input_text, encoding="utf-8")

if update_audio:
    text_to_mp3(input_text, OUTPUT_MP3_FILE)


if blank_input or edit_mode:
    with st.form("text_to_speech_form", border=False):
        input_text = st.text_area(
            "Enter text here:",
            value=input_text,
            placeholder="Enter text here",
            label_visibility="collapsed",
            height=300,
        )
        if st.form_submit_button("Read Aloud"):
            if input_text.strip():
                INPUT_TXT_FILE.write_text(input_text, encoding="utf-8")
                st.session_state["edit_mode"] = False
                st.rerun()

else:
    new_or_edit_clicked = st_btn_group(
        buttons=[{"label": "New", "value": "New"}, {"label": "Edit", "value": "Edit"}]
    )
    if new_or_edit_clicked == "New":
        INPUT_TXT_FILE.write_text("", encoding="utf-8")
        st.rerun()
    elif new_or_edit_clicked == "Edit":
        st.session_state["edit_mode"] = True
        st.rerun()

    st.audio(OUTPUT_MP3_FILE.read_bytes(), format="audio/mp3", autoplay=update_audio)


    # TODO how to escape html in input_text so it is safe ?
    st.html(f'<pre style="white-space: pre-wrap;">{input_text}</pre>')
