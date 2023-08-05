class SaveS3FileError(Exception):
    """
        Exception raised when save a file with data loaded return an error
        Attributes:
            bucket -- name of the bucket that file represents
            filename -- name of the file
    """
    def __init__(self, bucket, filename):
        self.bucket = bucket
        self.filename = filename
