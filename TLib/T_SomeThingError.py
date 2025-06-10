class SomeThingError(Exception):
    def __init__(self, message):
        self.message = message
    def __str__(self):
        return self.message

class SomeThingErrorList():
    NOTADMIN=0
    FILENOTFOUND=1