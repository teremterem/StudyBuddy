import os
from pathlib import Path
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from openai import OpenAI

import html2text
from dotenv import load_dotenv
from prompt_toolkit import HTML, PromptSession
from prompt_toolkit.document import Document
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.keys import Keys
from prompt_toolkit.lexers import Lexer
from prompt_toolkit.styles import Style
from pypdf import PdfReader


load_dotenv()


def text_to_mp3(input_txt: str, output_mp3_file: str, openai_client: Optional["OpenAI"] = None) -> None:
    if openai_client is None:
        from openai import OpenAI

        openai_client = OpenAI()

    response = openai_client.audio.speech.create(
        model=os.getenv("TTS_MODEL", "tts-1"),
        voice=os.getenv("TTS_VOICE", "alloy"),
        input=input_txt,
    )

    print(Path(output_mp3_file).resolve())  # TODO either remove this print or make it a logger
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


def prompt_text(prompt_purpose: str = "") -> str:
    # TODO use click.echo instead of print ?
    print(
        "\033[92;1m\n"
        f"Press Enter to submit text{prompt_purpose}.\n"
        "Press Ctrl+Space to insert a newline.\n"
        'Press Ctrl+C (or type "exit") to quit.\n'
        "\033[0m"
    )
    user_input = _prompt_session.prompt(
        HTML("<user_utterance>ENTER TEXT:\n\n</user_utterance>"),
        multiline=True,
        key_bindings=_prompt_bindings,
        lexer=_CustomPromptLexer(),
        style=_user_prompt_style,
    )
    return user_input


_user_prompt_style = Style.from_dict({"user_utterance": "fg:ansibrightyellow bold"})

_prompt_session = PromptSession()

_prompt_bindings = KeyBindings()


@_prompt_bindings.add(Keys.Enter)
def _prompt_binding_enter(event):
    event.current_buffer.validate_and_handle()


@_prompt_bindings.add(Keys.ControlSpace)
def _prompt_binding_control_space(event):
    event.current_buffer.insert_text("\n")


class _CustomPromptLexer(Lexer):
    """
    Custom lexer that paints user utterances in yellow (and bold).
    """

    def lex_document(self, document: Document):
        """
        Lex the document.
        """
        return lambda i: [("class:user_utterance", document.text.split("\n")[i])]
