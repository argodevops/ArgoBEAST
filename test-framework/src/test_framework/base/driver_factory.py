from selenium import webdriver


class WebDriverFactory():
    def __init__(self, config):
        self.driver = None
        self.options = None
        self.config = config

    def create_driver(self):
        self.options = webdriver.ChromeOptions()
        if self.config["headless"]:
            self.options.add_argument("--headless-new")

        # width and height.
        width, height = self.config["window_size"].split(",")
        self.options.add_argument(f"--window-size={width},{height}")

        # Initiate driver with waits and timeouts
        self.driver = webdriver.Chrome(options=self.options)
        self.driver.implicitly_wait(self.config["implicit_wait"])
        self.driver.set_page_load_timeout(self.config['page_load_timeout'])

        # Call base url
        self.driver.get(self.config["base_url"])

        return self.driver

    def quit_driver(self):
        if self.driver:
            self.driver.quit()
