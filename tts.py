import traceback

import streamlit as st

from study_buddy import text_to_mp3, INPUT_TXT_FILE, OUTPUT_TXT_FILE, OUTPUT_MP3_FILE


PAGE_TITLE = "Text-to-Speech"
st.set_page_config(page_title=PAGE_TITLE, layout="wide")

if not INPUT_TXT_FILE.exists():
    INPUT_TXT_FILE.touch()  # in case the user wants to use a different editor to enter text

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
regenerate_audio = updated_input or (not OUTPUT_MP3_FILE.exists() and not blank_input)

error_generating_audio = None
if regenerate_audio:
    try:
        text_to_mp3(input_text, OUTPUT_MP3_FILE)
        if updated_input:
            OUTPUT_TXT_FILE.write_text(input_text, encoding="utf-8")
    except Exception as e:
        traceback.print_exc()  # TODO replace with logger
        error_generating_audio = f"ERROR GENERATING AUDIO: {e}"

autoplay_audio = st.session_state.get("autoplay_audio")
if not autoplay_audio:
    # if audio was updated, autoplay it
    # (otherwise, autoplay it only if it's not the very first time the page is loaded)
    autoplay_audio = regenerate_audio
    # we always autoplay audio if the page is not loaded for the first time
    # (in this case we assume that the user is already actively interacting with the page)
    st.session_state["autoplay_audio"] = True

# ACTUAL PAGE CONTENT STARTS HERE

st.header(PAGE_TITLE)

if blank_input or edit_mode:
    new_input_text = st.text_area(
        "Enter text here:",
        value=input_text,
        placeholder="Enter text here",
        label_visibility="collapsed",
        height=300,
    )
    if new_input_text != input_text or st.button("Read Aloud"):
        st.session_state["edit_mode"] = False
        INPUT_TXT_FILE.write_text(new_input_text, encoding="utf-8")
        st.rerun()

else:
    with st.sidebar:
        if st.button("New"):
            INPUT_TXT_FILE.write_text("", encoding="utf-8")
            st.rerun()
        if st.button("Edit"):
            st.session_state["edit_mode"] = True
            st.rerun()

    if error_generating_audio:
        st.error(error_generating_audio)
    else:
        st.audio(OUTPUT_MP3_FILE.read_bytes(), format="audio/mp3", autoplay=autoplay_audio)

    # TODO how to escape html in input_text so it is safe ?
    st.html(f'<pre style="white-space: pre-wrap;">{input_text}</pre>')
