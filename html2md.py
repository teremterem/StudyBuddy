import traceback
from typing import Optional

import click

from study_buddy import html_to_md


@click.command()
@click.argument("input_html", type=click.Path(exists=True, dir_okay=False))
@click.option("--output", "-o", "output_md", type=click.Path(dir_okay=False), default=None)
def main(input_html: str, output_md: Optional[str]) -> None:
    try:
        html_to_md(input_html, output_md)
        click.echo(f"Successfully converted {input_html} to {output_md}")
    except Exception:
        traceback.print_exc()
        raise click.Abort()


if __name__ == "__main__":
    main()
