import logging
import sys
import AI_Devs

def initLoggers() -> None:
    level = logging.DEBUG
    root = logging.getLogger()
    root.setLevel(level)

    stdoutFormatter = logging.Formatter('[%(asctime)s][%(name)s][%(levelname)s] - %(message)s - [%(module)s/%(filename)s::%(funcName)s:%(lineno)d]')
    stdoutHandler = logging.StreamHandler(sys.stdout)
    stdoutHandler.setLevel(level)
    stdoutHandler.setFormatter(stdoutFormatter)

    root.addHandler(stdoutHandler)

def lesson1() -> None:
    print('Lesson 01 - helloapi')

    if len(sys.argv) == 1:
        raise RuntimeError('Missing apiKey argument')

    apiKey = sys.argv[1]
    ai = AI_Devs.AI_Devs(apiKey)
    ai.authorize('helloapi')
    task = ai.getTask()
    print('The task is: ', task['msg'])
    ai.answer(task['cookie'])

if __name__ == '__main__':
    initLoggers()

    try:
        lesson1()
    except Exception as exception:
        logging.error(exception, exc_info=True)
        exit(1)
