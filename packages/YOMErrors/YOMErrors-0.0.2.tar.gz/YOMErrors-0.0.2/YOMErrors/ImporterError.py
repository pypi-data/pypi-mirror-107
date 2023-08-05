
class ImporterError(Exception):
    """
        Exception raised when yom api service return an error
        Attributes:
            name -- error name
            status_code -- http response error code
    """
    def __init__(self, message, status=None, data=None):
        self.message = message
        self.status = status
        self.data = data
