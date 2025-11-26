from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver


class WebDriverFactory():
    def __init__(self, config):
        self.driver: WebDriver | None = None
        self.options = None
        self.config = config

    def create_driver(self):
        """
        Create and return a WebDriver instance based on the configuration
        :return: WebDriver instance
        """

        self.options = webdriver.ChromeOptions()

        if self.config["headless"]:
            self.options.add_argument("--headless=new")

        # width and height
        width, height = self.config["window_size"].split(",")
        self.options.add_argument(f"--window-size={width},{height}")

        # Shared args for Docker / Gitpod
        self.options.add_argument("--no-sandbox")
        self.options.add_argument("--disable-dev-shm-usage")

        if "remote_url" in self.config and self.config["remote_url"]:
            # Running inside Docker / Gitpod
            self.driver = webdriver.Remote(
                command_executor=self.config["remote_url"],
                options=self.options
            )
        else:
            # Local laptop mode
            self.driver = webdriver.Chrome(options=self.options)

        self.driver.implicitly_wait(self.config["implicit_wait"])
        self.driver.set_page_load_timeout(self.config['page_load_timeout'])
        self.driver.get(self.config["base_url"])

        return self.driver

    def quit_driver(self):
        if self.driver:
            self.driver.quit()
