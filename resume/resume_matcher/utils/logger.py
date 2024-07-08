import logging


def get_handlers(
    filename="app.log", mode="w", file_level=logging.DEBUG, stderr_level=logging.DEBUG
):

    # Stream handler
    stderr_handler = logging.StreamHandler()
    stderr_handler.setLevel(stderr_level)
    stderr_handler.setFormatter(CustomFormatter())

    # File handler
    file_handler = logging.FileHandler(filename, mode=mode)
    file_handler.setLevel(file_level)
    file_handler.setFormatter(CustomFormatter(True))

    # TODO: Add RotatingFileHandler

    return stderr_handler, file_handler


class CustomFormatter(logging.Formatter):
   

    def __init__(self, file=False):
       
        super().__init__()
        yellow = "\x1b[36;10m" if not file else ""
        blue = "\x1b[35;10m" if not file else ""
        green = "\x1b[32;10m" if not file else ""
        red = "\x1b[31;10m" if not file else ""
        bold_red = "\x1b[31;1m" if not file else ""
        reset = "\x1b[0m" if not file else ""
        log = "%(asctime)s (%(filename)s:%(lineno)d) - %(levelname)s: "
        msg = reset + "%(message)s"

        self.FORMATS = {
            logging.DEBUG: blue + log + msg,
            logging.INFO: green + log + msg,
            logging.WARNING: yellow + log + msg,
            logging.ERROR: red + log + msg,
            logging.CRITICAL: bold_red + log + msg,
        }

    def format(self, record):
        
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


def init_logging_config(
    basic_log_level=logging.INFO,
    filename="app.log",
    mode="w",
    file_level=logging.DEBUG,
    stderr_level=logging.DEBUG,
):
   
    logger = logging.getLogger()
    logger.setLevel(basic_log_level)

    # Get the handlers
    stderr_handler, file_handler = get_handlers(
        file_level=file_level, stderr_level=stderr_level, filename=filename, mode=mode
    )

    # Add the handlers
    logger.addHandler(stderr_handler)
    logger.addHandler(file_handler)
