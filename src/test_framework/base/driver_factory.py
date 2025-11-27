from selenium import webdriver


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

    def create_driver(self):
        """
        Create and return a new WebDriver instance based on config.
        """
        options = webdriver.ChromeOptions()

        # Headless mode
        if self.config.get("headless", False):
            options.add_argument("--headless=new")

        # Window size
        if "window_size" in self.config:
            width, height = self.config["window_size"].split(",")
            options.add_argument(f"--window-size={width},{height}")

        # Remote mode (Docker/Selenium Grid)
        remote_url = self.config.get("remote_url", "")
        if remote_url:
            driver = webdriver.Remote(
                command_executor=remote_url,
                options=options
            )
        else:
            # Local laptop mode
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
