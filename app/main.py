import logging
import os
import sys
import AI_Devs
from lessons import Lesson01
from lessons import Lesson02

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
            lessonNumber = input("""
Which lesson do you want to run?
1 - helloapi
2 - moderation

""")
        else:
            lessonNumber = sys.argv[1]

        if '1' == lessonNumber:
            lesson = Lesson01.Lesson01(ai)
        elif '2' == lessonNumber:
            lesson = Lesson02.Lesson02(ai)
        else:
            raise RuntimeError('Unknown lesson "{}"'.format(lessonNumber))

        lesson.run()

    except Exception as exception:
        logging.error(exception, exc_info=True)
        exit(1)
