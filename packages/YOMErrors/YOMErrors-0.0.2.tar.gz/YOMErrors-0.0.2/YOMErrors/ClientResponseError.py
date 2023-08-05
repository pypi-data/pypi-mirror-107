class ClientResponseError(Exception):
    """
        Exception raised when client service return an error
        Attributes:
            url -- url name, ex: www.movilvendor.com/api/get/clients
            status_code -- http response error code
    """
    def __init__(self, url, status_code):
        self.url = url
        self.status_code = status_code
