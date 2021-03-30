import logging


class GoogleValidationError(Exception):

    logging.exception(f'Google Validation Error{Exception}')  # pylint: disable=Use lazy % formatting in logging functions (logging-fstring-interpolation)


class BingValidationError(Exception):
    logging.exception(f'Bing Validation Error{Exception}')  # pylint: disable=Use lazy % formatting in logging functions (logging-fstring-interpolation)


class DDGValidationError(Exception):
    logging.exception(f'DDG Validation Error{Exception}')  #  pylint: disable=Use lazy % formatting in logging functions (logging-fstring-interpolation)
