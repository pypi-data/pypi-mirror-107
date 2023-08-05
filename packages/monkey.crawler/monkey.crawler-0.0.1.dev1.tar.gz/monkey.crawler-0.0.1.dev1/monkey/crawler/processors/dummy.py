# -*- coding: utf-8 -*-

from monkey.crawler.op_codes import OpCode

from monkey.crawler.processor import Processor, Reviser


class DummyDumpProcessor(Processor):

    def __init__(self, source_name: str, output_file_path: str, revisers: list[Reviser] = []):
        super().__init__(source_name, revisers)
        self.output_file_path = output_file_path
        self.output_file = open(output_file_path, 'w')

    def _process(self, record):
        self.output_file.write(str(record) + '\n')
        return OpCode.SUCCESS
