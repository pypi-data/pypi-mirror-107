# -*- coding: utf-8 -*-

import csv

from monkey.crawler.crawler import Crawler
from monkey.crawler.processor import Processor


class CSVCrawler(Crawler):

    def __init__(self, source_name: str, handler: Processor, source_file: str, offset: int = 1,
                 source_encoding: str = 'ansi', source_delimiter: str = ',', source_quote_char: str = '"',
                 col_heads_on_first_row: bool = True, col_heads: list[str] = None):
        super().__init__(source_name, handler, offset)
        self.encoding = source_encoding
        self.delimiter = source_delimiter
        self.quote_char = source_quote_char
        self.csv_file = source_file
        self.col_heads_on_first_row = col_heads_on_first_row
        # TODO: Avoid to open file before start to crawl
        with open(self.csv_file, encoding=self.encoding) as source:
            self.rows = list(csv.reader(source, delimiter=self.delimiter, quotechar=self.quote_char))
            self.row_count = len(self.rows)
            self.col_count = len(self.rows[0])
        if col_heads:
            # if len(col_heads) < self.col_count:
            #   raise an error
            self.col_heads = col_heads[:]
        elif self.col_heads_on_first_row:
            self.col_heads = self.rows[0][:]

    def _read_record(self, record_num):
        record = {}
        for col_num in range(0, self.col_count - 1):
            record[self.col_heads[col_num]] = self.rows[record_num][col_num]
        return record

    def _count_records(self):
        return self.row_count - self.offset

    def _echo_start(self):
        self.logger.info(
            f'Crawling {self.source_name} from {self.csv_file} file. \n\tFound {self.row_count - self.offset} rows '
            f'by {self.col_count} columns')
