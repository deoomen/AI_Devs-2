import logging
import sys

def initLoggers() -> None:
    level = logging.DEBUG
    root = logging.getLogger()
    root.setLevel(level)

    stdoutFormatter = logging.Formatter('[%(asctime)s][%(name)s][%(levelname)s] - %(message)s - [%(module)s/%(filename)s::%(funcName)s:%(lineno)d]')
    stdoutHandler = logging.StreamHandler(sys.stdout)
    stdoutHandler.setLevel(level)
    stdoutHandler.setFormatter(stdoutFormatter)

    root.addHandler(stdoutHandler)

if __name__ == '__main__':
    initLoggers()
    print('Hello')
