import streamlit as st

from study_buddy import text_to_mp3, INPUT_TXT_FILE, OUTPUT_TXT_FILE, OUTPUT_MP3_FILE


if not INPUT_TXT_FILE.exists():
    INPUT_TXT_FILE.touch()  # in case the user wants to use a different editor to enter text

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

first_run = st.session_state.get("first_run", True)
if first_run:
    st.session_state["first_run"] = False

blank_input = not input_text.strip()
updated_input = not blank_input and input_text != output_text
edit_mode = st.session_state.get("edit_mode", False)
update_audio = updated_input or (not OUTPUT_MP3_FILE.exists() and not blank_input)

if updated_input:
    OUTPUT_TXT_FILE.write_text(input_text, encoding="utf-8")

if update_audio:
    text_to_mp3(input_text, OUTPUT_MP3_FILE)


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

    st.audio(OUTPUT_MP3_FILE.read_bytes(), format="audio/mp3", autoplay=update_audio or not first_run)

    # TODO how to escape html in input_text so it is safe ?
    st.html(f'<pre style="white-space: pre-wrap;">{input_text}</pre>')
