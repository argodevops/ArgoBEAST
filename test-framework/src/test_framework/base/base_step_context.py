
class BaseStepContext():
    def __init__(self, context):
        self.context = context
        self.driver = context.driver
        self.config = context.config

    def get_page(self, PageClass):
        return PageClass(self.driver, self.config)

    def get_actions(self, ActionsClass):
        page = self.get_page(ActionsClass.PageClass)
        return ActionsClass(page)
