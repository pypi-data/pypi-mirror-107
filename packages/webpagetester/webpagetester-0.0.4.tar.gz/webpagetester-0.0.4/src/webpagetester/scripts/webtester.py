from ..pagetester import *
import multiprocessing as mp
import click
import pathlib

found = []
special = []
not_found = []


def process(i, page, report):
    if report:
        fname = str(i)
        fname += ".html"
        code, reason = test_page(page, fname)
    else:
        code, reason = test_page(page)

    return i, code, reason, page


def collect_result(result):
    i, code, reason, page = result
    if code:
        line = str(code) + "    " + page + "    " + reason + "\n"
        if code < 400:
            line = str(i) + "\t" + line
            global found
            found.append((i, line))
        else:
            global special
            special.append(line)
    else:
        global not_found
        not_found.append(page + "\n")

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

    global found
    global not_found
    global special

    found = []
    not_found = []
    special = []

    pool = mp.Pool(mp.cpu_count())
    report = out or screen
    for i, page in enumerate(pages):
        pool.apply_async(process, args=(i, page, report), callback=collect_result)

    pool.close()
    pool.join()

    found.sort(key=lambda x: x[0])
    found = [r for i, r in found]

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
