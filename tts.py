import traceback
from pathlib import Path
from typing import Optional

import click

from study_buddy import text_to_mp3, prompt_text


@click.command()
@click.argument("txt_file", type=click.Path(exists=True, dir_okay=False), required=False)
@click.option("--output", "-o", "output_mp3", type=click.Path(dir_okay=False), default=None)
def main(txt_file: Optional[str], output_mp3: Optional[str]) -> None:
    try:
        if txt_file is None:
            if output_mp3 is None:
                output_mp3 = "temp.mp3"  # TODO timestamp and hash
            input_txt = prompt_text(" for TTS")

        else:
            if output_mp3 is None:
                output_mp3 = txt_file + ".mp3"
            input_txt = Path(txt_file).read_text(encoding="utf-8")

        text_to_mp3(input_txt, output_mp3)
        click.echo(f"Audio saved to {output_mp3}")
    except Exception:
        traceback.print_exc()
        raise click.Abort()


if __name__ == "__main__":
    main()
