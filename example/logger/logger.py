#  -------------------------------
#  Difficult Rocket
#  Copyright © 2020-2023 by shenjackyuanjie 3695888@qq.com
#  All rights reserved
#  -------------------------------

from lib_not_dr.logger.logger import Logger

if __name__ == '__main__':
    logger = Logger.get_logger_by_name('test')
    logger.global_level = 0

    logger.info('Hello World!')

    logger.fine('Hello World!')
    logger.debug('Hello World!')
    logger.trace('Hello World!')
    logger.warn('Hello World!')
    logger.error('Hello World!')
    logger.fatal('Hello World!')
