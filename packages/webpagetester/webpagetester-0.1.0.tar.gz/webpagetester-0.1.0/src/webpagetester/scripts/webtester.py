from ..pagetester import *
import multiprocessing as mp
import click
import pathlib

found = []
special = []
not_found = []
counter = 0


def store_to_file(file: pathlib.Path):
    import json
    print("Saving ...", end="")
    store = dict(counter=counter, found=found, special=special, not_found=not_found)

    with file.open("w+") as writer:
        json.dump(store, writer, indent=4)
    print("DONE")


def load_from_file(file: pathlib.Path):
    print("Loading ...", end="")
    import json
    with file.open("r") as reader:
        res = json.load(reader)
    print("DONE")
    return res


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


from .. import __version__


@click.command(help="v"+__version__)
@click.option('-p', '--page', type=click.STRING, help='Page to test.', multiple=True)
@click.option('-f', '--file', type=click.STRING, help='A file with a url in each line.', multiple=True)
@click.option('-o', '--out', type=click.STRING, help='A file to store or append the report.')
@click.option('-', '--imaging', default=False, help='Will save the html response in a separate files.')
@click.option('-s', '--save', default=500, help='Will save the html response in a separate files.')
def console_testing(page, file, out, imaging, save):
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
    global counter

    tmp_file = pathlib.Path("tmp.json")
    if tmp_file.exists():
        res = load_from_file(tmp_file)
        found = res["found"]
        not_found = res["not_found"]
        special = res["special"]
        counter = res["counter"]
    else:
        found = []
        not_found = []
        special = []
        counter = 0

    pool = mp.Pool(mp.cpu_count())
    report = out or imaging
    for i, page in enumerate(pages, start=counter):
        try:
            pool.apply_async(process, args=(i, page, report), callback=collect_result)
        except KeyboardInterrupt:
            pool.terminate()
            print("Terminating!")
            import sys
            sys.exit(1)
        if i % save == 0:
            pool.close()
            pool.join()
            counter = i + 1
            store_to_file(tmp_file)
            pool = mp.Pool(mp.cpu_count())

    pool.close()
    pool.join()
    store_to_file(tmp_file)

    print("Sorting ...", end="")
    found.sort(key=lambda x: x[0])
    found = [r for i, r in found]
    print("DONE")

    if out:
        print("Creating Report...", end="")
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
        print("DONE")

    print("Cleaning up...", end="")
    tmp_file.unlink()
    print("DONE")

    input("Press Enter to close...")
