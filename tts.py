import traceback
from typing import Optional

import click
from dotenv import load_dotenv

from study_buddy import text_to_mp3


load_dotenv()


@click.command()
@click.argument("input_text", type=click.Path(exists=True, dir_okay=False))
@click.option("--output", "-o", "output_mp3", type=click.Path(dir_okay=False), default=None)
def main(input_text: str, output_mp3: Optional[str]) -> None:
    try:
        if output_mp3 is None:
            output_mp3 = input_text + ".mp3"

        text_to_mp3(input_text, output_mp3)
        click.echo(f"Successfully converted {input_text} to {output_mp3}")
    except:
        traceback.print_exc()
        raise click.Abort()


if __name__ == "__main__":
    main()
