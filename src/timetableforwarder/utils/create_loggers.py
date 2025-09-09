from logging import (
    Logger,
    getLogger,
    Formatter,
    FileHandler,
    WARNING,
    ERROR,
    StreamHandler
)


def create_main_logger() -> Logger:
    logger = getLogger('root')
    logger.setLevel(WARNING)

    fh = FileHandler('secret_data/main_logs.log')
    fh.setLevel(WARNING)

    ch = StreamHandler()
    ch.setLevel(ERROR)

    formatter = Formatter('%(asctime)s - %(levelname)s\n'
                          '%(message)s\n\n')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    logger.addHandler(fh)
    logger.addHandler(ch)

    return logger


def create_action_logger() -> Logger:
    logger = getLogger('action_logger')
    logger.setLevel(WARNING)

    fh = FileHandler('secret_data/action_logs.log')
    fh.setLevel(WARNING)

    formatter = Formatter('%(asctime)s - %(levelname)s\n'
                          '%(message)s\n\n')
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    logger.propagate = False
    return logger

