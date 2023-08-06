__version__ = "0.1.0"

from logging import handlers
import socket
import logging
from logging.handlers import RotatingFileHandler
import os, sys
from logger_es_handler.handlers import ESHandler

handlers = set()


class MyFilter(logging.Filter):
    def __init__(self, param=None):
        self.param = param

    def filter(self, record):
        if self.param is None:
            allow = True
        else:
            allow = self.param not in record.msg
        if allow:
            record.level = record.levelname
            # delattr(record, 'levelname')
            record.host = socket.gethostname()
            record.hostIp = socket.gethostbyname(record.host)

        return allow


logger = logging.getLogger(__name__)
logger.addFilter(MyFilter())
logger.setLevel(logging.DEBUG)


def logger_factory(
    funcname,
    kibana_config,
    environment,
    project_name,
    exclude="",
    path_log_file="/tmp",
    enable_console_log=True,
    enable_file_log=False,
    enable_es_log=True,
    send_debug=False,
    exclude_default=True,
):

    if exclude:
        exclude = exclude.split(",")
    else:
        exclude = []
    if exclude_default:
        exclude += [
            "pathname",
            "exc_info",
            "exc_text",
            "thread",
            "threadName",
            "stack_info",
            "filename",
            "processName",
            "process",
            "args",
            "msg",
            "name",
            "levelname",
        ]

    exclude_tuple = tuple(set(exclude))

    if enable_file_log:

        if not os.path.exists(f"{path_log_file}"):
            os.makedirs(f"{path_log_file}")

        handler_local = RotatingFileHandler(
            f"{path_log_file}/{funcname}.log", mode="a", maxBytes=50000, backupCount=10
        )

        formatter = logging.Formatter(
            "[%(levelname)s] %(asctime)s %(funcName)s %(message)s"
        )

        handler_local.setLevel(logging.DEBUG)
        handler_local.setFormatter(formatter)

        handlers.add(handler_local)

    if enable_console_log:

        handler_console = logging.StreamHandler(sys.stdout)

        formatter = logging.Formatter(
            "[%(levelname)s] %(asctime)s [%(funcName)s:%(lineno)d] %(message)s"
        )

        handler_console.setLevel(logging.DEBUG)
        handler_console.setFormatter(formatter)

        handlers.add(handler_console)

    if enable_es_log:
        formatter = logging.Formatter(
            "[%(levelname)s] %(asctime)s %(funcName)s %(message)s"
        )
        handler_es = ESHandler(
            hosts=[
                {
                    "host": kibana_config["kibana_server"],
                    "port": kibana_config["kibana_server_port"],
                }
            ],
            auth_type=ESHandler.AuthType.BASIC_AUTH,
            auth_details=(
                kibana_config["kibana_username"],
                kibana_config["kibana_password"],
            ),
            use_ssl=kibana_config["kibana_ssl"],
            disabled_fields=exclude_tuple,
            verify_ssl=False if not environment == "PRODUCTION" else True,
            es_index_name=project_name,
            es_additional_fields={
                "project": project_name,
                "environment": environment,
            },
        )

        handler_es.setFormatter(formatter)
        if send_debug:
            handler_es.setLevel(logging.DEBUG)
        else:
            handler_es.setLevel(logging.INFO)
        handlers.add(handler_es)

    load_handlers()

    return logger


def load_handlers():
    for i_handler in handlers:
        if not i_handler in logger.handlers:
            logger.addHandler(i_handler)
