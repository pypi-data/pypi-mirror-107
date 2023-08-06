from ..pagetester import *
import sys
import click
import pathlib


@click.command()
@click.option('-p', '--page', type=click.STRING, help='Page to test.', multiple=True)
@click.option('-f', '--file', type=click.STRING, help='A file with a url in each line.')
@click.option('-o', '--out', type=click.STRING, help='A file to store or append the report.')
@click.option('-s', '--screen', default=False, help='Will save the html response in a separate files.')
def console_testing(page, file, out, screen):
    # execute only if run as a script
    pages = []
    if page:
        pages += page
    if file:
        file = pathlib.Path(file)
        if not file.exists():
            print("No file in:", file.absolute())
        else:
            lines = []
            with file.open("r") as reader:
                lines += reader.readlines()
            for line in lines:
                pages.append(line.replace("\n", ""))

    found = []
    not_found = []
    for page in pages:
        exists = False
        if screen:
            fname = page.replace(":", "#")
            fname = fname.replace("/", "$")
            fname = fname.replace(".", "-")
            fname += ".html"
            exists = test_page(page, fname)
        else:
            exists = test_page(page)

        if exists:
            found.append(page)
        else:
            not_found.append(page)

    if out:
        file = pathlib.Path(out)
        with file.open("a+") as writer:
            writer.write("FOUND:\n")
            writer.write("======\n")
            writer.writelines(found)
            writer.write("\n")
            writer.write("\n")
            writer.write("FOUND NOT:\n")
            writer.write("==========\n")
            writer.writelines(not_found)

    input("Press Enter to close...")