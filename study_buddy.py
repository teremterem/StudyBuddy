import os
from pathlib import Path
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from openai import OpenAI

import html2text
from dotenv import load_dotenv
from pypdf import PdfReader


load_dotenv()


def text_to_mp3(input_txt_file: str, output_mp3_file: str, openai_client: Optional["OpenAI"] = None) -> None:
    if openai_client is None:
        from openai import OpenAI

        openai_client = OpenAI()

    input_txt = Path(input_txt_file).read_text(encoding="utf-8")

    response = openai_client.audio.speech.create(
        model=os.getenv("TTS_MODEL", "tts-1"),
        voice=os.getenv("TTS_VOICE", "alloy"),
        input=input_txt,
    )

    response.write_to_file(output_mp3_file)


def pdf_to_text(input_pdf_file: str, output_txt_file: str) -> None:
    reader = PdfReader(input_pdf_file)

    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"

    with open(output_txt_file, "w", encoding="utf-8") as f:
        f.write(text)


def html_to_md(input_html_file: str, output_md_file: str) -> None:
    h = html2text.HTML2Text(bodywidth=0)

    html_content = Path(input_html_file).read_text(encoding="utf-8")
    text = h.handle(html_content)

    with open(output_md_file, "w", encoding="utf-8") as f:
        f.write(text)
