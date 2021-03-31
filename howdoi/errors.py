import logging


class GoogleValidationError(Exception):

    logging.exception('Google Validation Error %s ', Exception)


class BingValidationError(Exception):
    logging.exception('Bing Validation Error %s ', Exception)


class DDGValidationError(Exception):
    logging.exception('DDG Validation Error %s', Exception)
