import logging
import signal

from kikyopp.utils import configure_logger
from kikyopp.worker import BaseWorker

log = logging.getLogger(__name__)


def run_worker(worker, debug=False):
    log_level = 'debug' if debug else 'info'
    configure_logger('kikyopp', log_level)

    try:
        _set_signal_handlers(worker)
        worker.start()
    except Exception as e:
        log.error('Failed to start worker: %s', e, exc_info=True)


def _set_signal_handlers(worker: BaseWorker):
    def _exit(signum, frame):
        log.info('Received exit signal: %s', signum)
        worker.stop()

    signal.signal(signal.SIGINT, _exit)
    signal.signal(signal.SIGTERM, _exit)
