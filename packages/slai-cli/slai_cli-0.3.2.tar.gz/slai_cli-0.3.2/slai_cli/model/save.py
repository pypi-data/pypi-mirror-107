import json
import datetime
import time

from pathlib import Path
from jinja2 import Template

from slai_cli.modules.drive_client import DriveClient
from slai_cli import log
from slai_cli.create.local_config_helper import LocalConfigHelper
from slai_cli.constants import NOTEBOOK_TRAINER_PREFIX, DEFAULT_TRAINER_TIMEOUT_S


"""

Pulls the current notebook from google collab and creates a new 'trainer'
A trainer is a class that contains the code necessary to train a model.

Here we do the following:
    - pulls the most recent notebook from collab
    - parses the notebook contents
    - fills out a trainer template with the following data:
        - SLAI_CURRENT_MODEL_VERSION
        - SLAI_TRAINER_TIMEOUT
        - SLAI_TRAINER_CONTENTS
    - save that trainer to disk as models/{model_name}/{model_version_id}/trainer.py

"""


def pull_current_notebook(*, model_name):
    log.action("Downloading notebook from google drive.")

    local_config_helper = LocalConfigHelper()
    local_config = local_config_helper.get_local_config()

    # TODO: handle key not existing
    model_notebook_google_drive_file_id = local_config["models"][model_name][
        "model_notebook_google_drive_file_id"
    ]
    model_version_id = local_config["models"][model_name]["model_version_id"]

    cwd = Path.cwd()

    drive_client = DriveClient()
    drive_client.download_latest_model_notebook(
        local_path=f"{cwd}/models/{model_name}/{model_version_id}/notebook.ipynb",
        model_notebook_google_drive_file_id=model_notebook_google_drive_file_id,
    )

    log.action("Done.")
    return model_version_id


def _parse_notebook(*, model_name, model_version_id):
    """
    Parses notebook contents into a model trainer.
    """

    log.action("Parsing notebook cells.")

    notebook_data = None

    cwd = Path.cwd()
    notebook_path = f"{cwd}/models/{model_name}/{model_version_id}/notebook.ipynb"
    with open(notebook_path, "r") as f_in:
        notebook_data = json.load(f_in)

    output_source = []
    for cell in notebook_data["cells"]:
        for line in cell["source"]:
            if NOTEBOOK_TRAINER_PREFIX in line:
                output_source.extend(cell["source"])
                break

    import_lines = list(
        filter(
            lambda l: l.startswith("import ") or l.startswith("from "), output_source
        )
    )

    output_source = list(
        filter(
            lambda l: not l.startswith("import ") and not l.startswith("from "),
            output_source,
        )
    )

    output_source = list(
        filter(lambda l: NOTEBOOK_TRAINER_PREFIX not in l, output_source)
    )

    for idx in range(len(output_source)):
        if output_source[idx] != "\n":
            output_source[idx] = (" " * 8) + output_source[idx]

    imports = "".join(import_lines)
    trainer = "".join(output_source)

    log.action("Done.")

    return imports, trainer


def _populate_trainer_template(*, model_name, imports, trainer, model_version_id):
    populated_templates = {}
    template_files = ["trainer.py"]

    pwd = Path(__file__).parent

    template_variables = {
        "SLAI_MODEL_NAME": model_name,
        "SLAI_TRAINER_CREATED_AT": datetime.datetime.now().isoformat(),
        "SLAI_TRAINER_IMPORTS": imports,
        "SLAI_TRAINER_CONTENTS": trainer,
        "SLAI_CURRENT_MODEL_VERSION": model_version_id,
        "SLAI_TRAINER_TIMEOUT": DEFAULT_TRAINER_TIMEOUT_S,
    }

    # populate model template files
    for fname in template_files:
        log.action(f"Generating: {fname} ")
        template_contents = None

        with open(f"{pwd}/templates/{fname}", "r") as f_in:
            template_contents = f_in.read()
            t = Template(template_contents)
            rendered_template = t.render(**template_variables)

            populated_templates[fname] = rendered_template
            log.action("Done.")

    cwd = Path.cwd()

    with open(f"{cwd}/models/{model_name}/{model_version_id}/trainer.py", "w") as f_out:
        f_out.write(populated_templates["trainer.py"])


def save_model(model_name):
    log.info(f"Saving current model notebook state on {time.ctime()}")

    local_config_helper = LocalConfigHelper()
    local_config = local_config_helper.get_local_config()
    model_version_id = local_config["models"][model_name]["model_version_id"]

    imports, trainer = _parse_notebook(
        model_name=model_name, model_version_id=model_version_id
    )

    _populate_trainer_template(
        model_name=model_name,
        imports=imports,
        trainer=trainer,
        model_version_id=model_version_id,
    )
