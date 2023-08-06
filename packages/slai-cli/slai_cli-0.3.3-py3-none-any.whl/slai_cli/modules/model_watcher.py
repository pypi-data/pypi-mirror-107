import time
import sys
import click

from slai_cli.modules.stoppable_thread import StoppableThread
from slai_cli.constants import MODEL_WATCH_INTERVAL_S
from slai_cli import log
from slai_cli.model.save import save_model, pull_current_notebook

CYCLES_PER_DOWNLOAD = 5


class ModelWatcher(StoppableThread):
    def __init__(self, *args, **kwargs):
        self.model_name = kwargs.pop("model_name")
        self._cleanup()

        super(ModelWatcher, self).__init__(*args, **kwargs)

    def _cleanup(self):
        self.idx = 0

    def run(self):
        while not self.stopped():
            if self.idx % CYCLES_PER_DOWNLOAD == 0:
                click.clear()
                pull_current_notebook(model_name=self.model_name)
                save_model(model_name=self.model_name)
                self.idx = 0

            self.idx += 1
            time.sleep(MODEL_WATCH_INTERVAL_S)

        self._cleanup()
