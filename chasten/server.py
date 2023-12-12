"""Create and run a syslog remote server for debugging purposes."""

import logging
import logging.handlers
import socketserver

from chasten import constants, output

LOG_FILE = constants.server.Log_File
HOST = constants.server.Localhost
PORT = constants.server.Port

logger = logging.getLogger(constants.logger.Syslog)


class SyslogUDPHandler(socketserver.BaseRequestHandler):
    """Syslog UDP handler for receiving debugging messages."""

    def handle(self):
        """Receive a message and then display it in output and log it to a file."""
        global logger  # noqa: PLW0602
        # receive the message from the syslog logging client
        message = bytes.decode(
            self.request[0].strip(), encoding=constants.server.Utf8_Encoding
        )
        # remove not-printable characters that can appear in message
        enhanced_message = str(message).replace(
            constants.markers.Bad_Fifteen, constants.markers.Empty_String
        )
        enhanced_message = enhanced_message.replace(
            constants.markers.Bad_Zero_Zero, constants.markers.Empty_String
        )
        # display the message inside of the syslog's console
        output.console.print(enhanced_message)
        # write the logging message to a file using a rotating file handler
        logger.debug(enhanced_message)


def start_syslog_server():
    """Start a syslog server."""
    global logger  # noqa: PLW0602
    # always log all of the messages to a file
    logger.setLevel(logging.DEBUG)
    # create a RotatingFileHandler such that:
    # -- it is stored in a file
    # -- it can never be bigger than 1 MB
    # -- one backup is created when log file gets too big
    rotating_file_handler = logging.handlers.RotatingFileHandler(
        LOG_FILE,
        maxBytes=constants.server.Max_Log_Size,
        backupCount=constants.server.Backup_Count,
    )
    # add the rotating file handler to the logger
    logger.addHandler(rotating_file_handler)
    # startup the server and then let it run forever
    try:
        server = socketserver.UDPServer((HOST, PORT), SyslogUDPHandler)
        server.serve_forever(poll_interval=constants.server.Poll_Interval)
    # let the server crash and raise an error on SystemExit and IOError
    except SystemExit:
        raise
    except IOError:
        raise
    # display a diagnostic message when server is manually stopped
    except KeyboardInterrupt:
        output.console.print(constants.chasten.Server_Shutdown)
        output.console.print()
