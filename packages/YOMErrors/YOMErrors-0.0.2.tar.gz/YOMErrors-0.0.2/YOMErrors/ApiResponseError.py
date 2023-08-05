
class ApiResponseError(Exception):
    """
        Exception raised when yom api service return an error
        Attributes:
            name -- error name
            status_code -- http response error code
    """
    def __init__(self, url, message='Error YOM API'):
        self.url = url
        self.message = message
