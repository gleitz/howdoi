import logging


class GoogleValidationError(Exception):

    logging.exception(f'Google Validation Error{Exception}')


class BingValidationError(Exception):
    logging.exception(f'Bing Validation Error{Exception}')


class DDGValidationError(Exception):
    logging.exception(f'DDG Validation Error{Exception}')
