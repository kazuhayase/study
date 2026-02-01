import logging


class SpecificDataFilter(logging.Filter):
    def filter(self, record):
        return 'specific_data' in record.getMessage()

class TableFilter(logging.Filter):
    def filter(self, record):
        return 'Table' in record.getMessage() or 'Tabs' in record.getMessage()

class TextFilter(logging.Filter):
    def filter(self, record):
        return 'Text' in record.getMessage()

class ExceptionFilter(logging.Filter):
    def filter(self, record):
        return '[Exception]' in record.getMessage()