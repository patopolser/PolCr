from polcr.core import *

import sys
import os


if __name__ == "__main__":

    if len(sys.argv) < 2:
        print(f"Usage: python {sys.argv[0]} <file.polser>")
        exit()

    filename = sys.argv[1]

    filename = filename + ".polser" if not filename.endswith(".polser") else filename

    if not os.path.exists(filename):
        print(f"{filename}.polser not found")

    with open(filename, "r", encoding= "utf-8") as f:
        text = f.read().strip()
        f.close()

    result, error = run('<stdin>', text)

    if error:
        print(error.as_string())
        
    elif result:
        if len(result.elements) == 1:
            print(repr(result.elements[0]))
