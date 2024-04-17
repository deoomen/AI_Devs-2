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
from tasks import Task10
from tasks import Task11
from tasks.Task12_search import Task12
from tasks.Task13_people import Task13
from tasks.Task14_knowledge import Task14
from tasks.Task15_tools import Task15
from tasks.Task16_gnome import Task16
from tasks.Task17_ownapi import Task17
from tasks.Task18_ownapipro import Task18
from tasks.Task19_meme import Task19
from tasks.Task20_optimaldb import Task20
from tasks.Task21_google import Task21

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
10 - scraper
11 - whoami
12 - search
13 - people
14 - knowledge
15 - tools
16 - gnome
17 - ownapi
18 - ownapipro
19 - meme
20 - optimaldb
21 - google

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
        elif '10' == taskNumber:
            task = Task10.Task10(ai)
        elif '11' == taskNumber:
            task = Task11.Task11(ai)
        elif '12' == taskNumber:
            task = Task12.Task12(ai)
        elif '13' == taskNumber:
            task = Task13.Task13(ai)
        elif '14' == taskNumber:
            task = Task14.Task14(ai)
        elif '15' == taskNumber:
            task = Task15.Task15(ai)
        elif '16' == taskNumber:
            task = Task16.Task16(ai)
        elif '17' == taskNumber:
            task = Task17.Task17(ai)
        elif '18' == taskNumber:
            task = Task18.Task18(ai)
        elif '19' == taskNumber:
            task = Task19.Task19(ai)
        elif '20' == taskNumber:
            task = Task20.Task20(ai)
        elif '21' == taskNumber:
            task = Task21.Task21(ai)
        else:
            raise RuntimeError('Unknown task "{}"'.format(taskNumber))

        task.run()

    except Exception as exception:
        logging.exception(exception)
        exit(1)
