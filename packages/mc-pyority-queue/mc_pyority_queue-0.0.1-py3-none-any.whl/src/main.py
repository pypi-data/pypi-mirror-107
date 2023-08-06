# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from task_handler import *
import asyncio
import time
from logger.json_logger import Logger



if __name__ == '__main__':

    logger = Logger.get_logger_instance()
    task_handler = TaskHandler('job_type', 'task_type', 'http://localhost:8081', 'http://localhost:8080/heartbeat', 0.5, logger)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(task_handler.dequeue(5))
    #time.sleep(10)


    #loop.run_until_complete(task_handler.reject(1,1,False, 'my reason'))
    # loop.close()


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
