import logging
import os
import sys
import AI_Devs
from tasks import Task01
from tasks import Task02
from tasks import Task03
from tasks import Task04
from tasks import Task05
from tasks import Task06
from tasks import Task07
from tasks import Task08
from tasks import Task09

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
3 - blogger
4 - liar
5 - inprompt
6 - embedding
7 - whisper
8 - functions
9 - rodo

""")
        else:
            taskNumber = sys.argv[1]

        if '1' == taskNumber:
            task = Task01.Task01(ai)
        elif '2' == taskNumber:
            task = Task02.Task02(ai)
        elif '3' == taskNumber:
            task = Task03.Task03(ai)
        elif '4' == taskNumber:
            task = Task04.Task04(ai)
        elif '5' == taskNumber:
            task = Task05.Task05(ai)
        elif '6' == taskNumber:
            task = Task06.Task06(ai)
        elif '7' == taskNumber:
            task = Task07.Task07(ai)
        elif '8' == taskNumber:
            task = Task08.Task08(ai)
        elif '9' == taskNumber:
            task = Task09.Task09(ai)
        else:
            raise RuntimeError('Unknown task "{}"'.format(taskNumber))

        task.run()

    except Exception as exception:
        logging.error(exception, exc_info=True)
        exit(1)
