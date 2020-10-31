import threading
import logging

# logger
logger = logging.getLogger("root").getChild(__name__)


def scheduler(job) -> None:
    def target() -> None:
        while True:
            job()

    schedule = threading.Thread(target=target)
    logger.info("scheduler is implemented successfully")
    schedule.start()
