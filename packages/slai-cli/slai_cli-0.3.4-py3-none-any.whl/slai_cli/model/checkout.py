import os
import shutil

from columnar import columnar
from pathlib import Path

from slai.clients.model import get_model_client
from slai.clients.cli import get_cli_client
from slai.clients.project import get_project_client
from slai_cli.create.local_config_helper import LocalConfigHelper
from slai_cli import log


def _list_model_versions(model_versions):
    headers = ["index", "name", "id", "created"]
    data = [
        [
            index,
            mv["name"],
            mv["id"],
            mv["created"],
        ]
        for index, mv in enumerate(model_versions)
    ]
    try:
        table = columnar(data, headers, no_borders=True)
        log.info(table)
    except IndexError:
        log.warn("No model versions found.")
        return


def _create_local_version_path(
    *, model_name, new_model_version_id, previous_model_version_id
):
    log.action("Copying existing model notebook...")

    cwd = Path.cwd()
    os.makedirs(f"{cwd}/models/{model_name}/{new_model_version_id}")

    notebook_to_copy = Path(
        f"{cwd}/models/{model_name}/{previous_model_version_id}/notebook.ipynb"
    )
    new_notebook = Path(
        f"{cwd}/models/{model_name}/{new_model_version_id}/notebook.ipynb"
    )

    shutil.copy(notebook_to_copy, new_notebook)
    with open(new_notebook) as f_in:
        _text = f_in.read().replace(previous_model_version_id, new_model_version_id)

    with open(new_notebook, "w") as f_out:
        f_out.write(_text)


def checkout_model_version(model_name, version_name=None):
    log.action(f"Retrieving model versions for model: {model_name}")

    project_client = get_project_client(project_name=None)
    project_name = project_client.get_project_name()

    model_client = get_model_client(model_name=model_name, project_name=project_name)
    cli_client = get_cli_client()

    model_id = model_client.model["id"]
    model_versions = cli_client.list_model_versions(model_id=model_id)
    version_names = {mv["name"]: mv["id"] for mv in model_versions}

    local_config_helper = LocalConfigHelper()
    local_model_config = local_config_helper.get_local_model_config(
        model_name=model_name, model_client=model_client
    )
    model_version_id = local_model_config["model_version_id"]

    # if a version name was specified, check if a version with that name exists
    if version_name is not None:

        # if so, just update local_config to point to that version
        if version_name in version_names:
            model_version_id_to_checkout = version_names[version_name]
            local_config_helper.checkout_model_version(
                model_name=model_name, model_version_id=model_version_id_to_checkout
            )

            log.action(f"Checked out model version: {version_name}")

        # otherwise, create a new model version with that name
        else:
            model_version = cli_client.create_model_version(
                model_id=model_id, name=version_name
            )
            model_version_id_to_checkout = model_version["id"]
            local_config_helper.checkout_model_version(
                model_name=model_name, model_version_id=model_version_id_to_checkout
            )

            _create_local_version_path(
                model_name=model_name,
                new_model_version_id=model_version_id_to_checkout,
                previous_model_version_id=model_version_id,
            )

            log.action(f"Checked out model version: {model_version['name']}")

    # if no version was specified, allow a user to checkout from existing model versions
    else:
        _list_model_versions(model_versions)
        model_version_index = log.action_prompt(
            "Checkout a version by index", type=int, default=0
        )
        if model_version_index < len(model_versions):
            model_version = model_versions[model_version_index]
            log.action(f"Checked out model version: {model_version['name']}")

            model_version_id_to_checkout = model_version["id"]
            local_config_helper.checkout_model_version(
                model_name=model_name, model_version_id=model_version_id_to_checkout
            )
        else:
            log.warn("Invalid model version.")
