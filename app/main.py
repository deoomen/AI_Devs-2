import logging
import os
import sys
import AI_Devs
from tasks import Task01
from tasks import Task02

def initLoggers() -> None:
    level = logging.INFO
    root = logging.getLogger()
    root.setLevel(level)

    stdoutFormatter = logging.Formatter('[%(asctime)s][%(name)s][%(levelname)s] - %(message)s - [%(module)s/%(filename)s::%(funcName)s:%(lineno)d]')
    stdoutHandler = logging.StreamHandler(sys.stdout)
    stdoutHandler.setLevel(level)
    stdoutHandler.setFormatter(stdoutFormatter)

    root.addHandler(stdoutHandler)

if __name__ == '__main__':
    initLoggers()

    try:
        apiKey = os.getenv('API_KEY')
        ai = AI_Devs.AI_Devs(apiKey)

        if 1 == len(sys.argv):
            taskNumber = input("""
Which task do you want to run?
1 - helloapi
2 - moderation

""")
        else:
            taskNumber = sys.argv[1]

        if '1' == taskNumber:
            task = Task01.Task01(ai)
        elif '2' == taskNumber:
            task = Task02.Task02(ai)
        else:
            raise RuntimeError('Unknown task "{}"'.format(taskNumber))

        task.run()

    except Exception as exception:
        logging.error(exception, exc_info=True)
        exit(1)
