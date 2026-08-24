import os
import sys

from kbank_statement_extract.main import extract


def main() -> None:
    filename = sys.argv[1]
    password = os.environ["PASSWORD"]

    if not filename or not password:
        raise ValueError("please provide filename and password")
    extract(filename, password)

if __name__ == '__main__':
    main()