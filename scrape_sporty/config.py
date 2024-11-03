from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from contextlib import contextmanager

@contextmanager
def edge_driver_generator():
    """Generator that yields a Selenium Edge WebDriver instance."""
    options = Options()
    # options.add_argument(
    #     "--headless"
    # )  # Run in headless mode if you don't need a visible browser

    driver_service = Service(
        EdgeChromiumDriverManager().install()
    )  # Automatically downloads the GeckoDriver

    try:
        driver = webdriver.Edge(service=driver_service, options=options)
        driver.maximize_window()
        yield driver
    finally:
        driver.quit()
