import os
from pathlib import Path
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from openai import OpenAI

import html2text
from dotenv import load_dotenv
from pypdf import PdfReader


load_dotenv()


def text_to_mp3(
    input_txt_file: str, output_mp3_file: Optional[str] = None, openai_client: Optional["OpenAI"] = None
) -> None:
    if openai_client is None:
        from openai import OpenAI

        openai_client = OpenAI()

    input_txt = Path(input_txt_file).read_text(encoding="utf-8")

    response = openai_client.audio.speech.create(
        model=os.getenv("TTS_MODEL", "tts-1"),
        voice=os.getenv("TTS_VOICE", "alloy"),
        input=input_txt,
    )

    if output_mp3_file is None:
        output_mp3_file = input_txt_file + ".mp3"

    response.write_to_file(output_mp3_file)


def pdf_to_text(input_pdf_file: str, output_txt_file: Optional[str] = None) -> None:
    reader = PdfReader(input_pdf_file)

    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"

    if output_txt_file is None:
        output_txt_file = input_pdf_file + ".txt"

    with open(output_txt_file, "w", encoding="utf-8") as f:
        f.write(text)


def html_to_md(input_html_file: str, output_md_file: Optional[str] = None) -> None:
    h = html2text.HTML2Text(bodywidth=0)

    html_content = Path(input_html_file).read_text(encoding="utf-8")
    text = h.handle(html_content)

    if output_md_file is None:
        output_md_file = input_html_file + ".md"

    with open(output_md_file, "w", encoding="utf-8") as f:
        f.write(text)
