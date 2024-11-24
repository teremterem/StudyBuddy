import traceback
from typing import Optional

import click

from study_buddy import pdf_to_text, INPUT_TXT_FILE


@click.command()
@click.argument("input_pdf", type=click.Path(exists=True, dir_okay=False))
@click.option("--output", "-o", "output_txt", type=click.Path(dir_okay=False), default=None)
def main(input_pdf: str, output_txt: Optional[str]) -> None:
    try:
        if output_txt is None:
            output_txt = INPUT_TXT_FILE

        pdf_to_text(input_pdf, output_txt)
        click.echo(f"Successfully converted {input_pdf} to {output_txt}")
    except Exception:
        traceback.print_exc()
        raise click.Abort()


if __name__ == "__main__":
    main()
