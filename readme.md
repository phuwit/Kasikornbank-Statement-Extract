# Kasikorn Bank Statement Extractor
extracting [date, time, txn_type, amount, balance, description] from kasikorn bank pdf statement with password (provided by user) into text then into csv as needed

## Setting up

- create a venv and activate it
- install the required dependency: pypdfium2
```bash
pip install pypdfium2
```

- accquire a kasikorn bank pdf statement

## Usage

### extract transactions into text
```bash
python extract.py {pdf_filename} {password}
```
the script will create a file with {pdf_filename}.txt

### convert text to csv
**user should manually check that each line contain exactly 1 transaction before proceeding**
sometimes with long description the pdf would have 2 lines per transaction. please fix that manually.
also that is why it is a seperate script.
```bash
python format.py {txt_filename} {password}
```
the script will create a file with {txt_filename}.csv
