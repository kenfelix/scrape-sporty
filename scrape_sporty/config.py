from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from contextlib import contextmanager


@contextmanager
def chrome_driver_generator():
    """Generator that yields a Selenium Chrome WebDriver instance."""
    options = Options()
    options.add_argument("--headless")  # Run in headless mode
    options.add_argument("--no-sandbox")  # Required for Replit
    options.add_argument(
        "--disable-dev-shm-usage"
    )  # Avoid issues with limited resources

    driver_service = Service(
        ChromeDriverManager().install()
    )  # Automatically downloads the GeckoDriver

    try:
        driver = webdriver.Chrome(service=driver_service, options=options)
        driver.maximize_window()
        yield driver
    finally:
        driver.quit()
