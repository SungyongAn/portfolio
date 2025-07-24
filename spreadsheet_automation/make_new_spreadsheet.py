import gspread
from pathlib import Path

gc = gspread.oauth(
    credentials_filename=Path.home(),
)

sh = gc.create("test00001")
