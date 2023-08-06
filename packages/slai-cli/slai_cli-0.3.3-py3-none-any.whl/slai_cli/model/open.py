import click
import time

from pathlib import Path
from slai.clients.model import get_model_client
from slai.clients.project import get_project_client

from slai_cli.create.local_config_helper import LocalConfigHelper
from slai_cli.modules.model_watcher import ModelWatcher
from slai_cli.modules.drive_client import DriveClient
from slai_cli import log
from slai_cli.constants import MODEL_WATCH_INTERVAL_S


def _upload_local_notebook(model_client, model_name):
    local_config_helper = LocalConfigHelper()

    local_model_config = local_config_helper.get_local_model_config(
        model_name=model_name, model_client=model_client
    )

    model_notebook_google_drive_file_id = local_model_config.get(
        "model_notebook_google_drive_file_id"
    )
    model_google_drive_folder_id = local_model_config.get(
        "model_google_drive_folder_id"
    )
    model_version_id = local_model_config.get("model_version_id")

    cwd = Path.cwd()

    drive_client = DriveClient()
    model_notebook_google_drive_file_id = drive_client.upload_model_notebook(
        model_name=model_name,
        model_google_drive_folder_id=model_google_drive_folder_id,
        notebook_path=f"{cwd}/models/{model_name}/{model_version_id}/notebook.ipynb",
        file_id=model_notebook_google_drive_file_id,
    )

    return model_notebook_google_drive_file_id


def open_model(name, watch):
    log.action("Opening notebook on collab.")

    project_client = get_project_client(project_name=None)
    model_client = get_model_client(
        model_name=name, project_name=project_client.get_project_name()
    )
    model_notebook_google_drive_file_id = _upload_local_notebook(
        model_client=model_client, model_name=name
    )

    click.launch(
        f"https://colab.research.google.com/drive/{model_notebook_google_drive_file_id}"
    )

    if watch:
        model_watching_thread = ModelWatcher(
            model_name=name,
        )
        model_watching_thread.daemon = True
        model_watching_thread.start()

        while True:
            try:
                time.sleep(MODEL_WATCH_INTERVAL_S)
            except KeyboardInterrupt:
                model_watching_thread.stop()
                model_watching_thread.join()
                break

        log.action("Goodbye.")
