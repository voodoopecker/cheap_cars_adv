from loguru import logger as LOGGER

LOGGER.add('logs/debug.log', format='{time}|{level}|{module}.{function}:{line} - {message}', level='DEBUG', rotation='00:00', compression='zip')

def main():
    LOGGER.success('Started')


if __name__ == '__main__':
    main()
