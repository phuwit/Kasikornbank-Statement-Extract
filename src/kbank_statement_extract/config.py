import re
from typing import Dict, Literal

from .classes import BoundingBox

ROWS_PER_PAGE = 46
BBOX_ROW_HEIGHT = 11.955
EXTRACTED_BBOX_KEYS = Literal[
    "date",
    "time",
    "description",
    "amount",
    "withdrawal_check",
    "balance",
    "channel",
    "details",
]
FIRST_ROW_BBOX_TOP_OFFSET = 192.948
FIRST_ROW_BBOX_CONFIG: Dict[EXTRACTED_BBOX_KEYS, BoundingBox] = {
    "date": BoundingBox(width=27.750, top=FIRST_ROW_BBOX_TOP_OFFSET, left=66.125),
    "time": BoundingBox(width=27.750, top=FIRST_ROW_BBOX_TOP_OFFSET, left=94.125),
    "description": BoundingBox(
        width=79.750, top=FIRST_ROW_BBOX_TOP_OFFSET, left=122.125
    ),
    "amount": BoundingBox(
        width=67.750, top=FIRST_ROW_BBOX_TOP_OFFSET, left=202.125
    ),
    "withdrawal_check": BoundingBox(
        width=18.000, top=FIRST_ROW_BBOX_TOP_OFFSET, left=251.875
    ),
    "balance": BoundingBox(
        width=61.750, top=FIRST_ROW_BBOX_TOP_OFFSET, left=270.125
    ),
    "channel": BoundingBox(
        width=70.750, top=FIRST_ROW_BBOX_TOP_OFFSET, left=332.125
    ),
    "details": BoundingBox(
        width=131.750, top=FIRST_ROW_BBOX_TOP_OFFSET, left=403.125
    ),
}
EXTRACTED_ROW_IS_WITHDRAWAL_REGEX: Dict[EXTRACTED_BBOX_KEYS, re.Pattern[str]] = {
    "withdrawal_check": re.compile(r".+")
}
EXTRACTED_ROW_IGNORE_REGEX: Dict[EXTRACTED_BBOX_KEYS, re.Pattern[str]] = {
    "description": re.compile(r"Beginning Balance")
}