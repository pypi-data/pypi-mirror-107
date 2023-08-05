#!/usr/bin/python
# -*- coding: utf-8 -*-

import getopt
import logging
import logging.config
import sys

from monkey.ioc.core import Registry

_CMD_LINE_HELP = '__main__.py -f <path to config file>'


def _read_opts(argv):
    config_file = 'config.json'
    try:
        opts, args = getopt.getopt(argv[1:], "?f:")
    except getopt.GetoptError as err:
        print(err)
        print(_CMD_LINE_HELP)
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-?':
            print(_CMD_LINE_HELP)
            sys.exit()
        elif opt in '-f':
            config_file = arg
    return config_file


def launch(argv):
    config_file = _read_opts(argv)

    registry = Registry()
    registry.load(config_file)

    try:
        logging_conf_file = registry.get('logging_conf', 'logging_conf')
        logging.config.fileConfig(logging_conf_file)
    except FileNotFoundError as e:
        print(e)

    crawlers = registry.get('crawlers')
    for crawler in crawlers:
        crawler.crawl()


if __name__ == '__main__':  # pragma: no coverage
    launch(sys.argv)
