"""
Base class for step context
"""


class BaseStepContext:
    def __init__(self, driver, config):
        self.driver = driver
        self.config = config

    def get_page(self, PageClass):  # pylint: disable=invalid-name
        """
        Get an instance of a page object
        :param PageClass: Class of the page object
        :return: Instance of the page object
        """
        return PageClass(self.driver, self.config)

    def get_actions(self, ActionsClass):  # pylint: disable=invalid-name
        """
        Get an instance of an actions object
        :param ActionsClass: Class of the actions object
        :return: Instance of the actions object
        """
        page = self.get_page(ActionsClass.PageClass)
        return ActionsClass(page)
