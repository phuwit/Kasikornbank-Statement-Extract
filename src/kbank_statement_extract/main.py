from pathlib import Path
from typing import Dict, List
import pypdfium2 as pdfium

from kbank_statement_extract.classes import Transaction
from kbank_statement_extract.config import (
    BBOX_ROW_HEIGHT,
    EXTRACTED_BBOX_KEYS,
    EXTRACTED_ROW_IGNORE_REGEX,
    EXTRACTED_ROW_IS_WITHDRAWAL_REGEX,
    FIRST_ROW_BBOX_CONFIG,
    FIRST_ROW_BBOX_TOP_OFFSET,
    ROWS_PER_PAGE,
)

ExtractedRow = Dict[EXTRACTED_BBOX_KEYS, str]


def extract_row(
    pageheight: float, textpage: pdfium.PdfTextPage, row_idx: int
) -> ExtractedRow:
    row: Dict[EXTRACTED_BBOX_KEYS, str] = {}
    for key, bbox in FIRST_ROW_BBOX_CONFIG.items():

        top = pageheight - (FIRST_ROW_BBOX_TOP_OFFSET + (BBOX_ROW_HEIGHT * row_idx))
        left = bbox.left
        bottom = top - BBOX_ROW_HEIGHT
        right = bbox.left + bbox.width

        value = textpage.get_text_bounded(  # type: ignore
            left=left,
            bottom=bottom,
            right=right,
            top=top,
        )
        row[key] = value

    return row


def is_row_ignored(row: ExtractedRow) -> bool:
    for key, value in EXTRACTED_ROW_IGNORE_REGEX.items():
        if value.match(row[key]) is not None:
            return True
    return False


def is_withdrawal(row: ExtractedRow) -> bool:
    for key, value in EXTRACTED_ROW_IS_WITHDRAWAL_REGEX.items():
        if value.match(row[key]) is not None:
            return False
    return True


def is_merge_with_previous(row: ExtractedRow) -> bool:
    if not row["date"] and not row["time"] and not row["amount"] and not row["balance"]:
        return True
    return False


def clean_text(text: str) -> str:
    return (text.replace(",", "")).strip()


def format_extracted_row_to_transactions(row: ExtractedRow):
    withdrawal = is_withdrawal(row)
    if withdrawal:
        txn_type = "withdrawal"
    else:
        txn_type = "deposit"
    return Transaction(
        date=clean_text(row["date"]),
        time=clean_text(row["time"]),
        description=clean_text(row["description"]),
        txn_type=txn_type,
        withdrawal=withdrawal,
        amount=clean_text(row["amount"]),
        balance=clean_text(row["balance"]),
        channel=clean_text(row["channel"]),
        details=clean_text(row["details"]),
    )


def extract(filename: str, password: str) -> None:
    pdf = pdfium.PdfDocument(input=filename, password=password)

    extracted_rows: List[ExtractedRow] = []
    for page in pdf:
        textpage = page.get_textpage()
        _, height = page.get_size()
        for row_idx in range(ROWS_PER_PAGE):
            extracted_row = extract_row(
                pageheight=height, textpage=textpage, row_idx=row_idx
            )

            if is_row_ignored(extracted_row):
                continue

            if is_merge_with_previous(extracted_row):
                for key, value in extracted_row.items():
                    if not value:
                        continue
                    extracted_rows[-1][key] = f"{extracted_rows[-1][key]} {value}"
                continue

            extracted_rows.append(extracted_row)

    transactions = map(format_extracted_row_to_transactions, extracted_rows)
    filecontents: str = (
        Transaction.get_csv_header()
        + "\n"
        + "\n".join(map(lambda t: str(t), transactions))
    )
    with open(Path(filename).with_suffix('.csv'), mode="wt") as file:
        file.write(filecontents)
