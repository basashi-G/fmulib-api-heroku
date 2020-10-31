"""
Use this module when you want logging through multple file.

Usage
1. Import this module.
2. Import "logging" module.
3. make "log" dir.
4. make logger like this "logger = logging.getLogger("root").getChild(__name__)".
"""
import logging
from logging import getLogger, StreamHandler, Formatter

FORMAT = "[%(levelname)s]:%(asctime)s:%(name)s -> %(message)s"

logger = getLogger("root")
logger.setLevel(logging.DEBUG)

stream_hander = StreamHandler()
stream_hander.setLevel(logging.DEBUG)
stream_hander.setFormatter(Formatter("%(message)s"))

logger.addHandler(stream_hander)

"""
file_handler = FileHandler("/var/log/flask/logger.log")
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(Formatter(FORMAT))

logger.addHandler(file_handler)
"""
