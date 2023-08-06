# -*- coding: utf-8 -*-

"""
日志功能
"""

from loguru import logger
import sys
import re


def init_log(sdkConfig):
    log_file_max_size = sdkConfig.log_file_max_size
    log_file_max_number = sdkConfig.log_file_max_number
    logger.remove(handler_id=None)
    output_format = "{time:YYYY-MM-DD HH:mm:ss} {level:5} ({file}:{line}) {thread.name} - {message}"
    clear_output_format = "{message}"

    def filter_lllll(message):
        return re.match(r"(.+\|){5}", message['message'])

    def filter_ll(message):
        return re.match(r"^([^|]+\|){2}[^|]+$", message['message'])

    logger.add("logs/service.log", format=output_format, rotation=str(log_file_max_size) + " MB", retention=log_file_max_number, filter="")
    logger.add("logs/stat.log", format=clear_output_format, rotation=str(log_file_max_size) + " MB", retention=log_file_max_number, filter=filter_lllll)
    logger.add("logs/recognize_stat.log", format=clear_output_format, rotation=str(log_file_max_size) + " MB", retention=log_file_max_number, filter=filter_ll)
    logger.add(sys.stdout, format=output_format)



