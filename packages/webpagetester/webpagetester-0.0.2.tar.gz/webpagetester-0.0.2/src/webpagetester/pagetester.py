import requests
from pathlib import Path


def test_page(url: str, file=None):
    try:
        request = requests.get(url)
        if request.status_code == 200:
            if file:
                file = Path(file)
                print(url, 'Web site exists', file.name)
                with file.open("wb+") as writer:
                    writer.write(request.content)
            else:
                print(url, 'Web site exists')
            return True
        else:
            print(url, 'Web site does not exist')
            return False
    except requests.exceptions.ConnectionError:
        print(url, 'Web site does not exist')
        return False


def test_file(fname: str):
    file = Path(fname)
    if not file.exists():
        print("Could not find file:", file.absolute())

    lines = []
    with file.open("r") as reader:
        lines = reader.readlines()
    ffile = open(create_name(fname, "_found"), "w")
    nffile = open(create_name(fname, "_not_found"), "w")
    for line in lines:
        line = line.replace('\n', '')
        exists = test_page(line)
        if exists:
            ffile.write(line + "\n")
        else:
            nffile.write(line + "\n")

    ffile.close()
    nffile.close()


def create_name(fname: str, key: str):
    parts = fname.split(".")
    name = ""
    for i in range(0, len(parts) - 1):
        name = name + parts[i]

    name = name + key + "." + parts[-1]
    return name