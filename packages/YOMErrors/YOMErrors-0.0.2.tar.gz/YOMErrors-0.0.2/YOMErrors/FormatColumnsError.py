from YOMLogger import YOMLogger

class FormatColumnsError(Exception):
    """
        Exception raised when column of file does not exists.
        Attributes:
            file -- name of the file
            column -- list of dicts that contains now valid columns and current type vs valid type
            column --> ex: [{columnName: 'clientId', currentType: 'integer', validType: 'string'}}]
    """
    def __init__(self, file, columns):
        self.file = file
        self.columns = columns
        self.logger = YOMLogger()
        self.logger.error(self.__str__())

    def __str__(self):
        error_message = ''
        for column in self.columns:
            error_message += f"\n Column {column['columnName']} must be: {column['validType']}, received: {column['currentType']}"

        return error_message
