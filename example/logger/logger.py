#  -------------------------------
#  Difficult Rocket
#  Copyright © 2020-2023 by shenjackyuanjie 3695888@qq.com
#  All rights reserved
#  -------------------------------

from lib_not_dr.logger.logger import Logger

import logging

def logging_logger() -> None:

    logger = logging.getLogger('test')
    logger.setLevel(logging.DEBUG)

    logger.info('Hello World!')
    logger.debug('Hello World!')
    logger.warning('warnnnnnnn')
    logger.error('Hello World!')
    logger.fatal('good bye world')  # critical


def lndl_logger() -> None:
    logger = Logger.get_logger_by_name('test')
    logger.global_level = 0

    logger.info('Hello World!')
    logger.fine('Hello World!')
    logger.debug('Hello World!')
    logger.trace('Hello tracing!')
    logger.warn('warnnnnnnn')
    logger.error('Hello World!')
    logger.fatal('good bye world')


def main():
    logger = Logger.get_logger_by_name('test')
    logger.global_level = 0

    logger.info('Hello World!')
    logger.fine('Hello World!')
    logger.debug('Hello World!')
    logger.trace('Hello tracing!')
    logger.warn('warnnnnnnn')
    logger.error('Hello World!')
    logger.fatal('good bye world')

    logger.info('this message if from tag', tag='test')
    logger.debug('this debug log if from admin', tag='admin')
    logger.debug('and this message ends with none', end=' ')
    logger.trace('so this message will be in the same line', tag='same line!')
    logger.info('so just info some stuff')


if __name__ == '__main__':
    lndl_logger()
    logging_logger()
