import win32com.client as win32
from PIL import ImageGrab, Image
import numpy as np
import datetime as dt
from os.path import join, exists
from os import mkdir, listdir
import pandas as pd
from robot import PATH
from settings import REPORT_NAME, CHECKLIST_NAME, REPORT_PROCESSED
import xlwings as xw


def build_checklist_dataframe() -> pd.DataFrame:

    today = dt.datetime.today()

    df = pd.read_csv(join(PATH, f"{CHECKLIST_NAME}{today.strftime('%Y%m%d')}.csv"), sep=';',
                     encoding='latin1', encoding_errors='ignore', skiprows=4)

    # Column names in numpy array
    columns = df.columns.values
    columns = np.append(columns, ["Resultado"])

    # Extract column of users from data
    users = df['Usuario Creación']

    # Filter users by number of records existing.
    users_count = users.value_counts()
    # If a user has more than one record, it will be included as a user who has completed checklist.
    users_checklist_complete = users_count[(
        users_count > 1).values].index.values
    # users_checklist_incomplete = users_count[(users_count == 1).values].index.values

    # Create a completed list for Series
    completed = ["COMPLETO" if row['Usuario Creación']
                 in users_checklist_complete else "INCOMPLETO" for index, row in df.iterrows()]

    # Create a completed Series to insert into df
    df.insert(df.shape[1], "RESULTADO", completed, allow_duplicates=True)

    return df


def build_values_dataframe() -> pd.DataFrame:
    df = pd.read_excel(join(PATH, REPORT_PROCESSED),
                       sheet_name='PT_RENDIMIENTO', skiprows=10, skipfooter=1)
    df['PROGRAMA'] = df['PROGRAMA'].replace(
        to_replace=r'TM_VA.|.+M_', value='', regex=True)
    return df


def insert_data(checklist_df: pd.DataFrame):
    # Load Workbook
    wb = xw.Book(join(PATH, REPORT_NAME))
    # Select DB_CHECKLIST worksheet and paste data from checklist
    xw.sheets["DB_CHECKLIST"].range("A2").options(
        index=False, header=False).value = checklist_df
    wb.save(join(PATH, REPORT_PROCESSED))
    # Select GRAFICOS PROGRAMA worksheet and paste data from values table
    values_df = build_values_dataframe()
    xw.sheets["GRAFICOS PROGRAMA"].range("A2").options(
        index=False, header=False).value = values_df
    wb.save(join(PATH, REPORT_PROCESSED))
    wb.close()


def refresh_charts():
    app = win32.Dispatch('Excel.Application')
    app.DisplayAlerts = False
    app.Visible = True

    excel_book = app.Workbooks.Open(join(PATH, REPORT_PROCESSED))

    # Refresh all pivot tables
    excel_book.RefreshAll()

    sheet = app.Sheets(3)

    if not exists(join(PATH, 'attachments')):
        mkdir(join(PATH, 'attachments'))

    for n, shape in enumerate(sheet.Shapes):

        # Save shape to clipboard, then save what is in the clipboard to the file
        shape.Copy()
        image = ImageGrab.grabclipboard()
        # Saves the image into the existing png file (overwriting) TODO ***** Have try except?
        image.save(join(PATH, 'attachments', f"image{n + 1}.png"), 'png')

    excel_book.Save()
    excel_book.Close()
    app.Quit()

    del excel_book
    del app


# def build_consolidated():
#     folders = listdir(PATH)
#     for folder in folders:
#         pass