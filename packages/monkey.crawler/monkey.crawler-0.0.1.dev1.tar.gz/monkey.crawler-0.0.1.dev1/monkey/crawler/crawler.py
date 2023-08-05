# -*- coding: utf-8 -*-

import logging

from monkey.crawler.op_codes import OpCode, OpCounter, Plotter
from monkey.crawler.processor import Processor


_MAX_RETRY_COUNT = 3


class Crawler:

    def __init__(self, source_name: str, handler: Processor, offset: int = 0):
        self.logger = logging.getLogger(self.__class__.__name__.lower())
        self.source_name = source_name
        self.offset = offset
        self.handler = handler
        self.retry_record_list = []
        self.retry_count = 0

    def crawl(self):
        """Crawl the entire data source"""
        allow_retry = self.retry_count <= _MAX_RETRY_COUNT
        counter = OpCounter()
        # TODO: Consideration should be given to sources where the number of records cannot be determined in advance.
        # TODO: Consideration should be given to sources that streams data
        self._echo_start()
        record_count = self._count_records()
        print(f'-- START ({self.source_name}) -> {record_count} records --', end='', flush=True)
        plotter = Plotter()
        for record_num in range(self.offset, record_count + self.offset):
            plotter.print_line_head(record_num - self.offset)
            record = self._read_record(record_num)
            op_code = self._handle_record(record, allow_retry)
            counter.inc(op_code)
            plotter.plot(op_code)
            if op_code == OpCode.RETRY:
                self.retry_record_list.append(record)
        print('\n-- END --')
        self._report(record_count, counter)
        if len(self.retry_record_list) > 0:
            self._crawl_retry_record_list()

    def _crawl_retry_record_list(self):
        self.retry_count += 1
        allow_retry = self.retry_count <= _MAX_RETRY_COUNT
        counter = OpCounter()
        # TODO : Replace by echo_start_retry
        # self._echo_start()
        record_list = self.retry_record_list
        self.retry_record_list = []
        record_count = len(record_list)
        print(f'-- RETRY ({self.source_name}) -> {record_count} records --', end='', flush=True)
        plotter = Plotter()
        for record_num in range(0, record_count):
            plotter.print_line_head(record_num)
            record = record_list[record_num]
            op_code = self._handle_record(record, allow_retry)
            counter.inc(op_code)
            plotter.plot(op_code)
            if op_code == OpCode.RETRY:
                self.retry_record_list.append(record)
        print('\n-- END --')
        # TODO: Refine report for retries
        self._report(record_count, counter)
        if len(self.retry_record_list) > 0 and self.retry_count <= _MAX_RETRY_COUNT:
            self._crawl_retry_record_list()

    def _read_record(self, record_num):
        raise NotImplementedError()

    def _handle_record(self, record, allow_retry):
        return self.handler.process(record, allow_retry=allow_retry)

    def _count_records(self):
        raise NotImplementedError()

    def _report(self, record_count, counter: OpCounter):
        miss_count = record_count - counter.total()
        self.logger.info(
            'Crawling report: \n{}\n\tMISSED    : {}\n\n'.format(counter, str(miss_count).rjust(4)))

    def _echo_start(self):
        raise NotImplementedError()
