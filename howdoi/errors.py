import logging


class GoogleValidationError(Exception):

    def __init__(self):
        logging.exception('Google Validation Error %s ', Exception)


class BingValidationError(Exception):

    def __init__(self):
        logging.exception('Bing Validation Error %s ', Exception)


class DDGValidationError(Exception):
    def __init__(self):
        logging.exception('DDG Validation Error %s', Exception)
