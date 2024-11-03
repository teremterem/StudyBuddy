import click
from pypdf import PdfReader
from typing import Optional
import os


@click.command()
@click.argument("input_pdf", type=click.Path(exists=True, dir_okay=False))
@click.option("--output", "-o", "output_txt", type=click.Path(dir_okay=False), default=None)
def main(input_pdf: str, output_txt: Optional[str]) -> None:
    try:
        # Create a PDF reader object
        reader = PdfReader(input_pdf)

        # Extract text from all pages
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"

        # If output_txt not provided, derive from input_pdf
        if output_txt is None:
            output_txt = input_pdf + ".txt"
        # Write the text to output file
        with open(output_txt, "w", encoding="utf-8") as f:
            f.write(text)

        click.echo(f"Successfully converted {input_pdf} to {output_txt}")

    except Exception as e:
        click.echo(f"Error converting PDF: {str(e)}", err=True)
        raise click.Abort()


if __name__ == "__main__":
    print("current working directory:", os.getcwd())
    main()
