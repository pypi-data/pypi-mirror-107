from ..pagetester import *
import sys
import click
import pathlib


@click.command()
@click.option('-p', '--page', type=click.STRING, help='Page to test.', multiple=True)
@click.option('-f', '--file', type=click.STRING, help='A file with a url in each line.', multiple=True)
@click.option('-o', '--out', type=click.STRING, help='A file to store or append the report.')
@click.option('-s', '--screen', default=False, help='Will save the html response in a separate files.')
def console_testing(page, file, out, screen):
    # execute only if run as a script
    pages = []
    if page:
        pages += page
    if file:
        for f in file:
            f = pathlib.Path(f)
            if not f.exists():
                print("No file in:", f.absolute())
            else:
                lines = []
                with f.open("r") as reader:
                    lines += reader.readlines()
                for line in lines:
                    pages.append(line.replace("\n", ""))

    found = []
    special = []
    not_found = []
    for page in pages:
        code = 0
        if out or screen:
            fname = str(len(found))
            fname += ".html"
            code, reason = test_page(page, fname)
        else:
            code, reason = test_page(page)

        if code:
            line = str(code) + "    " + page + "    " + reason + "\n"
            if code < 400:
                line = str(len(found))+"\t" + line
                found.append(line)
            else:
                special.append(line)
        else:
            not_found.append(page + "\n")

    if out:
        file = pathlib.Path(out)
        with file.open("w+") as writer:
            writer.write("FOUND:\n")
            writer.write("======\n")
            writer.writelines(found)
            writer.write("\n")
            writer.write("\n")
            writer.write("SPECIAL:\n")
            writer.write("=======\n")
            writer.writelines(special)
            writer.write("\n")
            writer.write("\n")
            writer.write("FOUND NOT:\n")
            writer.write("==========\n")
            writer.writelines(not_found)

    input("Press Enter to close...")