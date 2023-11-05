#  -------------------------------
#  Difficult Rocket
#  Copyright © 2020-2023 by shenjackyuanjie 3695888@qq.com
#  All rights reserved
#  -------------------------------

import time
import inspect

from lib_not_dr.logger.structure import LogMessage
from lib_not_dr.logger.outstream import FileCacheOutputStream, StdioOutputStream

if __name__ == '__main__':
    log_message = LogMessage(messages=['Hello World!'],
                             level=20,
                             stack_trace=inspect.currentframe(),
                             logger_tag='tester',
                             logger_name='test')

    file_cache = FileCacheOutputStream(file_name='test.log')
    stdio = StdioOutputStream()

    print(file_cache.as_markdown())
    print(stdio.as_markdown())

    file_cache.write_stdout(log_message)
    stdio.write_stdout(log_message)
    # wait for 10 sec
    print('wait for 11 sec')
    time.sleep(11)
    print('finish')
    # write 10 lines

    for i in range(10):
        log_message.log_time = time.time_ns()
        file_cache.write_stdout(log_message)
        stdio.write_stdout(log_message)

    print('write 10 lines')
    time.sleep(3)
    print('exit')
