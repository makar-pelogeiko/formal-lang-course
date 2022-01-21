class InterpError(Exception):
    def __init__(self, stack_lst: list, message="Exception occurred"):
        self.stack_lst = stack_lst
        self.message = message
        super().__init__(self.message)
