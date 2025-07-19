import gspread

gc = gspread.oauth(
    credentials_filename="OAuth.json",
)

sh = gc.create("test00001")
