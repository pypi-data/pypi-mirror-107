from datetime import datetime

class FileNotFoundError(Exception):
    """
        Exception raised when file does not exists.
        Attributes:
            file -- name of the file that file represents
            date -- 
    """
    def __init__(self, file, date=datetime.now()):
        self.file = file
        self.date = date
        
    def __str__(self):
        return f"No files found for {self.file} on date {self.date}."
