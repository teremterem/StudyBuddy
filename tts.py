import os
from pathlib import Path
from typing import Optional

import click
from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()


@click.command()
@click.argument("input_text", type=click.Path(exists=True, dir_okay=False))
@click.option("--output", "-o", "output_mp3", type=click.Path(dir_okay=False), default=None)
def main(input_text: str, output_mp3: Optional[str]) -> None:
    try:
        client = OpenAI()

        txt_content = Path(input_text).read_text(encoding="utf-8")

        response = client.audio.speech.create(
            model=os.getenv("TTS_MODEL", "tts-1"),
            voice=os.getenv("TTS_VOICE", "alloy"),
            input=txt_content,
        )

        if output_mp3 is None:
            output_mp3 = input_text + ".mp3"

        response.write_to_file(output_mp3)

        click.echo(f"Successfully converted {input_text} to {output_mp3}")

    except Exception as e:
        click.echo(f"Error converting text: {str(e)}", err=True)
        raise click.Abort()


if __name__ == "__main__":
    # print("current working directory:", os.getcwd())
    main()
