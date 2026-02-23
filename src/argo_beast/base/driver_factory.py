from selenium import webdriver
from selenium.webdriver.remote.client_config import ClientConfig
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
        page_load_strategy = self.config.get("page_load_strategy", "normal")
        if self.browser == "firefox":
            options = webdriver.FirefoxOptions()
            if self.config.get("headless", False):
                options.add_argument("--headless")
            options.set_capability("pageLoadStrategy", page_load_strategy)
        elif self.browser == "edge":
            options = webdriver.EdgeOptions()
            if self.config.get("headless", False):
                options.add_argument("--headless=new")
            options.set_capability("pageLoadStrategy", page_load_strategy)
        else:
            options = webdriver.ChromeOptions()
            if self.config.get("headless", False):
                options.add_argument("--headless=new")
            options.set_capability("pageLoadStrategy", page_load_strategy)

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
            remote_url = self.config.get("remote_url", "")
            
            timeout_val = self.config.get("grid_timeout", 60)

            if remote_url:
                grid_config = ClientConfig(remote_server_addr=remote_url, timeout=timeout_val) 
                
                driver = webdriver.Remote(
                    command_executor=remote_url,
                    options=options,
                    client_config=grid_config
                )
            else:
                driver_path = self.config.get("driver_path")
                service = self._create_service(driver_path) if driver_path else None
                driver = self._create_local_driver(options, service=service)

            # ... rest of your window sizing and implicit wait logic ...
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
