from pathlib import Path
from typing import Optional

import click
import html2text


@click.command()
@click.argument("input_html", type=click.Path(exists=True, dir_okay=False))
@click.option("--output", "-o", "output_md", type=click.Path(dir_okay=False), default=None)
def main(input_html: str, output_md: Optional[str]) -> None:
    try:
        h = html2text.HTML2Text(bodywidth=0)

        html_content = Path(input_html).read_text(encoding="utf-8")
        text = h.handle(html_content)

        # If output_md not provided, derive from input_html
        if output_md is None:
            output_md = input_html + ".md"
        # Write the text to output file
        with open(output_md, "w", encoding="utf-8") as f:
            f.write(text)

        click.echo(f"Successfully converted {input_html} to {output_md}")

    except Exception as e:
        click.echo(f"Error converting HTML: {str(e)}", err=True)
        raise click.Abort()


if __name__ == "__main__":
    # print("current working directory:", os.getcwd())
    main()
