import os
import yaml

from pathlib import Path
from slai_cli import log
from slai_cli.modules.drive_client import DriveClient
from slai.clients.project import get_project_client

LOCAL_CONFIG_PATH = ".slai/local_config.yml"


class LocalConfigHelper:
    def __init__(self):
        self.local_path = os.getcwd()
        self.drive_client = DriveClient()
        self.project_client = get_project_client(project_name=None)

    def check_local_config(self):
        self.project_name = self.project_client.get_project_name()
        self.project = self.project_client.get_project()
        self.service_name = f"{self.project['name']}-{self.project['id']}"

        self.local_config = self._load_local_config()

    def get_local_config(self):
        local_config = None

        with open(LOCAL_CONFIG_PATH, "r") as f_in:
            try:
                local_config = yaml.safe_load(f_in)
            except yaml.YAMLError:
                pass

        return local_config

    def get_local_model_config(self, *, model_name, model_client):
        local_config = self.get_local_config()

        if model_name not in local_config["models"].keys():
            log.action("Uploading template notebook to google drive.")

            cwd = Path.cwd()
            model_version_id = model_client.model["model_version_id"]

            model_google_drive_folder_id = self.drive_client.create_model_folder(
                model_name=model_name,
                project_google_drive_folder_id=local_config[
                    "project_google_drive_folder_id"
                ],
            )
            model_notebook_google_drive_file_id = self.drive_client.upload_model_notebook(
                model_name=model_name,
                model_google_drive_folder_id=model_google_drive_folder_id,
                notebook_path=f"{cwd}/models/{model_name}/{model_version_id}/notebook.ipynb",
            )

            self.update_local_model_config(
                model_name=model_name,
                model_google_drive_folder_id=model_google_drive_folder_id,
                model_notebook_google_drive_file_id=model_notebook_google_drive_file_id,
                model_version_id=model_version_id,
            )
            local_config = self.get_local_config()
            log.action("Done.")

        local_model_config = local_config["models"][model_name]
        return local_model_config

    def update_local_model_config(
        self,
        *,
        model_name,
        model_google_drive_folder_id,
        model_notebook_google_drive_file_id,
        model_version_id,
    ):
        local_config = self.get_local_config()

        model_config = {}
        model_config["model_google_drive_folder_id"] = model_google_drive_folder_id
        model_config[
            "model_notebook_google_drive_file_id"
        ] = model_notebook_google_drive_file_id
        model_config["model_version_id"] = model_version_id

        local_config["models"][model_name] = model_config

        with open(LOCAL_CONFIG_PATH, "w") as f_out:
            yaml.dump(local_config, f_out, default_flow_style=False)

    def checkout_model_version(
        self,
        *,
        model_name,
        model_version_id,
    ):
        local_config = self.get_local_config()
        local_config["models"][model_name]["model_version_id"] = model_version_id

        with open(LOCAL_CONFIG_PATH, "w") as f_out:
            yaml.dump(local_config, f_out, default_flow_style=False)

    def _load_local_config(self):
        if not os.path.exists(LOCAL_CONFIG_PATH):
            log.info(
                "No local configuration found, creating new file and uploading configuration."
            )
            project_folder_id = self._create_google_drive_folder()

            config_data = {
                "project_google_drive_folder_id": project_folder_id,
                "models": {},
            }

            with open(LOCAL_CONFIG_PATH, "w") as f_out:
                yaml.dump(config_data, f_out, default_flow_style=False)

    def _create_google_drive_folder(self):
        log.action("Creating project folder in google drive")

        project_folder_id = self.drive_client.create_project_folder(
            folder_name=f"slai-{self.service_name}"
        )

        log.action("Done.")

        return project_folder_id
