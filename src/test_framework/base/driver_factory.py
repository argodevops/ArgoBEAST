from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService


class WebDriverFactory:
    """
    A stateless driver factory.

    - Does NOT store `self.driver`
    - Does NOT hold WebDriver instances after creation
    - Returns a fresh driver object each time
    - Leaves all driver lifecycle management to environment.py
    """

    def __init__(self, config):
        self.config = config
        self.browser = config.get("browser")

    def create_driver(self):
        """
        Create and return a new WebDriver instance based on config.
        """

        if self.browser == "edge":
            options = webdriver.EdgeOptions()
        elif self.browser == "firefox":
            options = webdriver.FirefoxOptions()
        else:
            options = webdriver.ChromeOptions()

        # Headless mode
        if self.config.get("headless", False):
            options.add_argument("--headless=new")

        # Window size
        if "window_size" in self.config:
            width, height = self.config["window_size"].split(",")
            options.add_argument(f"--window-size={width},{height}")

        # Remote mode (Docker/Selenium Grid)
        driver_path = self.config.get("driver_path")
        remote_url = self.config.get("remote_url", "")
        service = None

        if driver_path:
            # If we have a path, we wrap it in a Service object
            if self.browser == "edge":
                service = EdgeService(executable_path=driver_path)
            elif self.browser == "firefox":
                service = FirefoxService(executable_path=driver_path)
            else:
                service = ChromeService(executable_path=driver_path)

        if remote_url:
            driver = webdriver.Remote(
                command_executor=remote_url,
                options=options
            )
        else:
            # Local laptop mode
            if self.browser == "edge":
                driver = webdriver.Edge(options=options, service=service)
            elif self.browser == "firefox":
                driver = webdriver.Firefox(options=options)
            else:
                driver = webdriver.Chrome(options=options)
        # Timeouts + ready state
        driver.implicitly_wait(self.config.get("implicit_wait", 5))
        driver.set_page_load_timeout(self.config.get("page_load_timeout", 30))

        # Navigate to base URL
        base_url = self.config.get("base_url")
        if base_url:
            driver.get(base_url)

        return driver

    def quit_driver(self, driver):
        """
        Optional helper for people who manage drivers outside Behave.
        Does nothing if the driver is already None or raises during quit.
        """
        if not driver:
            return

        try:
            driver.quit()
        except Exception:
            # Ignore "session already closed" errors
            pass
