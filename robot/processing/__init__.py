from .actions import *
import logging


def process_report():
    logging.info("Processing report started.")
    df = build_checklist_dataframe()
    insert_data(df)
    logging.info("Data checklist inserted into report.")
    refresh_charts()
    logging.info("Report charts refreshed succesfully.")
