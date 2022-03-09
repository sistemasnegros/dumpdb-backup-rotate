# -*- coding: utf-8 -*-
import logging


class Log(object):

    def __init__(self, config):
        level_log = logging.INFO

        if config.debug:
            level_log = logging.DEBUG

        logformat = "%(asctime)s %(levelname)s: %(message)s"

        logging.basicConfig(filename=config.logPath,
                            filemode='w', format=logformat, level=level_log)

        if config.verbose:
            stream_handler = logging.StreamHandler()
            log_formatter = logging.Formatter(logformat)
            stream_handler.setFormatter(log_formatter)
            logging.getLogger().addHandler(stream_handler)
