class CallBackDescriptor:
    def __set_name__(self, owner, name):
        self.callback_name = name

    def __set__(self, instance, value):
        if 

