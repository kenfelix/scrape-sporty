from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager
from contextlib import contextmanager

@contextmanager
def firefox_driver_generator():
    """Generator that yields a Selenium Firefox WebDriver instance."""
    options = Options()
    options.add_argument(
        "--headless"
    )  # Run in headless mode if you don't need a visible browser

    driver_service = Service(
        GeckoDriverManager().install()
    )  # Automatically downloads the GeckoDriver

    try:
        driver = webdriver.Firefox(service=driver_service, options=options)
        driver.maximize_window()
        yield driver
    finally:
        driver.quit()
