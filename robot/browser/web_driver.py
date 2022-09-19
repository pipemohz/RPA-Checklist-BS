from selenium.webdriver import Chrome


class WebDriver():
    def __init__(self, driver: Chrome) -> None:
        self.driver = driver

    def __enter__(self):
        return self.driver

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.quit()