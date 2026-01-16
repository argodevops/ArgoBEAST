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
        self.browser = config.get("browser", "chrome").lower()

    def _get_browser_options(self):
        """
        Internal helper to get browser options based on config.
        """
        if self.browser == "firefox":
            options = webdriver.FirefoxOptions()
            if self.config.get("headless", False):
                options.add_argument("--headless")
        elif self.browser == "edge":
            options = webdriver.EdgeOptions()
            if self.config.get("headless", False):
                options.add_argument("--headless=new")
        else:
            options = webdriver.ChromeOptions()
            if self.config.get("headless", False):
                options.add_argument("--headless=new")

        # Apply optional custom flags
        custom_flags = self.config.get("browser_args", [])
        if isinstance(custom_flags, list):
            for flag in custom_flags:
                options.add_argument(flag)

        return options

    def _create_local_driver(self, options, service=None):
        """
        Internal helper to create a local WebDriver instance.
        """
        if self.browser == "edge":
            return webdriver.Edge(options=options, service=service)
        elif self.browser == "firefox":
            return webdriver.Firefox(options=options, service=service)
        else:
            return webdriver.Chrome(options=options, service=service)

    def _create_service(self, driver_path):
        """
        Internal helper to create a Service object based on browser type.
        """
        if self.browser == "edge":
            return EdgeService(executable_path=driver_path)
        elif self.browser == "firefox":
            return FirefoxService(executable_path=driver_path)
        else:
            return ChromeService(executable_path=driver_path)

    def create_driver(self):
        """
        Create and return a new WebDriver instance based on config.
        """
        options = self._get_browser_options()

        # Remote mode (Docker/Selenium Grid)
        driver_path = self.config.get("driver_path")
        service = None

        if driver_path:
            # If we have a path, we wrap it in a Service object
            service = self._create_service(driver_path)

        remote_url = self.config.get("remote_url", "")
        if remote_url:
            driver = webdriver.Remote(
                command_executor=remote_url,
                options=options
            )
        # Local laptop mode
        else:
            driver = self._create_local_driver(options, service=service)

        # Window Size (Universal fallback for all browsers)
        if "window_size" in self.config:
            # Handles "1920,1080" and "1920, 1080" safely
            parts = self.config["window_size"].split(",")
            if len(parts) == 2:
                width = int(parts[0].strip())
                height = int(parts[1].strip())
                driver.set_window_size(width, height)

        # Timeouts + ready state
        driver.implicitly_wait(self.config.get("implicit_wait", 5))
        driver.set_page_load_timeout(self.config.get("page_load_timeout", 30))

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
