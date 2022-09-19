import logging
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from robot.manage_directories import report_downloaded
from settings import CLOUDFEET_URL, CLOUDFEET_USERNAME, CLOUDFEET_PASSWORD, MAX_TIME
import datetime as dt
import time


def login(driver: Chrome):
    try:
        driver.get(url=CLOUDFEET_URL)
        # Fill login form fields
        # Username input
        username = WebDriverWait(driver, 5).until(EC.element_to_be_clickable(
            (By.ID, "c_TxtUsuario")))
        username.send_keys(CLOUDFEET_USERNAME)
        # Password input
        password = WebDriverWait(driver, 5).until(EC.element_to_be_clickable(
            (By.ID, "c_TxtClave")))
        password.send_keys(CLOUDFEET_PASSWORD)
        # Login button
        login_button = WebDriverWait(driver, 5).until(EC.element_to_be_clickable(
            (By.ID, "c_cmdLogin")))
        login_button.click()

    except Exception as e:
        # print(f"The following exception has ocurred during login: {e}")
        logging.error(
            (f"An error has ocurred during report selection: {type(e)}"))
        raise(e)


def select_report(driver: Chrome):
    try:
        # Get and click navbar dropdown anchor tag element "Consultas"
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="CtlMenu1_Divmenu"]/div/div/div/ul[1]/li[5]/a'))).click()

        # Get and click element anchor tag element "Checklist"
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="ConsultasVehiculos_ConsultasChecklist"]/a'))).click()

        # Get reports-container
        reports = WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, 'div.reports-container a')))
        for report in reports:
            if report.find_element(By.CSS_SELECTOR, "h2").text.lower() == "consulta general":
                report.click()
                break
    except Exception as e:
        logging.error(
            (f"An error has ocurred during report selection: {type(e)}"))
        raise(e)


def set_exporting_filters(driver: Chrome):
    try:
        today = dt.datetime.today()
        delta = dt.timedelta(days=1)
        yesterday = today - delta

        # Set date interval to generate report.
        date_from_input = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.ID, "c_ctlFechaCreadoDesde_TxtFecha")))
        date_from_input.click()
        date_from_input.send_keys(yesterday.strftime("%d/%m/%Y"))

        date_to_input = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.ID, "c_ctlFechaCreadoHasta_TxtFecha")))
        date_to_input.click()
        date_to_input.send_keys(yesterday.strftime("%d/%m/%Y"))

        # Get list of fields to show in report generation
        fields_ul = WebDriverWait(driver, 5).until(EC.presence_of_element_located(
            (By.XPATH, '//*[@id="c_ctl00"]/div[4]/div[2]/ul')))
        fields = fields_ul.find_elements(By.CSS_SELECTOR, "li")

        required_fields = ["Número", "Vehículo", "Fecha Chequeo",
                           "Tipo", "Estado", "Usuario Creación", "Fecha Creación"]

        for field in fields:
            field_input = field.find_element(By.CSS_SELECTOR, "input")
            if field.text in required_fields:
                if field_input.get_attribute("checked") == "false":
                    driver.execute_script("arguments[0].click()", field_input)
            else:
                if field_input.get_attribute("checked") == "true":
                    driver.execute_script("arguments[0].click()", field_input)

    except Exception as e:
        logging.error(
            (f"An error has ocurred during settings filters: {type(e)}"))
        raise(e)


def export_report(driver: Chrome, path: str):
    try:
        # Click on generate button
        search_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.ID, "c_cmdBuscar")))
        driver.execute_script("arguments[0].click()", search_button)
        # search_button.click()

        # Click on export button
        export_data_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.ID, "c_ctlExportar_LnkExportToCSV")))
        driver.execute_script("arguments[0].click()", export_data_button)
        # export_button.click()

        # Select csv option radio button
        csv_radio_button = driver.find_element(By.ID, "c_ctlExportar_OptTexto")
        driver.execute_script("arguments[0].click()", csv_radio_button)

        # Get and click on export button in modal window.
        export_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.ID, "c_ctlExportar_cmdExportar")))
        driver.execute_script("arguments[0].click()", export_button)

        # Wait for download report to complete.
        tic = time.perf_counter()
        while time.perf_counter() - tic < MAX_TIME:
            if report_downloaded(path):
                break

    except Exception as e:
        logging.error(
            (f"An error has ocurred during report exporting: {type(e)}"))
        raise(e)
