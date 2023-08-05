# -*- coding: utf-8 -*-

import logging

from monkey.crawler.op_codes import OpCode


class RecoverableError(Exception):

    def __init__(self, message='Recoverable error', cause=None):
        self.message = message
        self.cause = cause


class InputError(Exception):

    def __init__(self, record_info, explanation='', cause=None):
        self.message = f'Bad input for record: {record_info} -> {explanation}'
        self.record_info = record_info
        self.cause = cause


class MissingRequiredFieldError(InputError):

    def __init__(self, record_info, missing_field_name):
        super().__init__(record_info, f'Required field {missing_field_name} is missing.')
        self.missing_field_name = missing_field_name


class ProcessingError(Exception):
    def __init__(self, record_info, explanation='', cause=None):
        self.message = f'Processing error for record: {record_info} -> {explanation}'
        self.record_info = record_info
        self.cause = cause


class Reviser:
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    def handle(self, record):
        raise NotImplemented()


class Processor:
    def __init__(self, source_name: str, revisers: list[Reviser] = None):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.source_name = source_name
        self.revisers = revisers

    def process(self, record, allow_retry=False):
        try:
            rec = self._prepare(record)
            if rec is None:
                op_code = OpCode.IGNORE
            else:
                op_code = self._process(rec)
        except RecoverableError as e:
            self.logger.error(f'{self.source_name} - RECOVERABLE ERROR - {e.message}')
            if allow_retry:
                op_code = OpCode.RETRY
            else:
                op_code = OpCode.ERROR
        except InputError as e:
            self.logger.error(f'{self.source_name} - INPUT ERROR - {e.message}')
            op_code = OpCode.ERROR
        except ProcessingError as e:
            self.logger.error(f'{self.source_name} - PROCESSING ERROR - {e.message}')
            op_code = OpCode.ERROR
        except Exception as e:
            self.logger.error(f'{self.source_name} - UNEXPECTED ERROR - {e}')
            op_code = OpCode.ERROR
        self.logger.log(op_code.get_default_logging_level(), f'{self.source_name} - {op_code.get_name()} - {record}')
        return op_code

    def _prepare(self, record):
        rec = record
        for reviser in self.revisers:
            rec = reviser.handle(rec)
            if rec is None:
                break
        return rec

    def _process(self, record):
        """Actual processing of a handled objet
        :param record: The record object to process
        :return: The executed operation code
        """
        raise NotImplemented()
