# Kasikorn Bank Statement Extractor
extracting date,time,description,txn_type,withdrawal,amount,balance,channel,details from kasikorn bank pdf statement with password into a csv

## Setting up

- install dependencies
```sh
uv sync
```

## Usage

### extract transactions into csv
```sh
PASSWORD={password} uv run extract {pdf_filename}
```
the script will create a file with {pdf_filename}.txt
