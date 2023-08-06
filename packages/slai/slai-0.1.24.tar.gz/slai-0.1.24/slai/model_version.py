import re
import importlib
import sys

from slai.dataset import DataSet
from slai.clients.model import get_model_client
from slai.exceptions import UnsupportedModelFormat, UnableToConvertNotebook
from slai.modules.model_saver import ModelSaver, ValidModelFrameworks
from slai.modules.runtime import detect_runtime, ValidRuntimes
from slai.modules import notebook_utils


class ModelVersion:
    def __init__(self, *, model_name, project_name, model_version_id=None):
        self.runtime = detect_runtime()

        self.model_name = model_name
        self.project_name = project_name

        self.model_client = get_model_client(
            model_name=self.model_name, project_name=self.project_name
        )
        self.project = self.model_client.project_client.get_project()
        self.model = self.model_client.get_model()

        if model_version_id is None:
            self.model_version_id = self.get_version()
        else:
            self.model_version_id = model_version_id

    def get_version(self):
        if self.model_version_id is None:
            self.model = self.model_client.get_model()
            self.model_version_id = self.model["model_version_id"]

        return self.model_version_id

    def dataset(self):
        return DataSet(model=self.model, model_version=self.model_version_id)

    def _get_framework_name(self, model):
        module = None

        if model is not None:
            _model_class = repr(model.__class__.__bases__[0])
            _matches = re.findall(r"\<class\s\'([a-zA-Z0-9\.]+)\'\>", _model_class)

            if len(_matches) >= 1:
                module = _matches[0].split(".")[0].upper()

        return module

    def _mount_google_drive(self):
        try:
            from google.colab import drive

            drive.mount("/content/drive", force_remount=True)
        except ImportError:
            raise

    def _handle_colab_trainer(self):
        self._mount_google_drive()

        _subprocess = importlib.import_module("subprocess")

        trainer_path = f"/content/drive/MyDrive/slai-{self.project_name}-{self.project['id']}/{self.model_name}/{self.model_name}.py"  # noqa
        notebook_path = f"/content/drive/MyDrive/slai-{self.project_name}-{self.project['id']}/{self.model_name}/{self.model_name}.ipynb"  # noqa

        return_code = _subprocess.call(
            f"jupyter nbconvert {notebook_path} --to=python", shell=True
        )
        if return_code != 0:
            raise UnableToConvertNotebook("could_not_convert_notebook")

        spec = importlib.util.spec_from_file_location("trainer", trainer_path)
        trainer_module = importlib.util.module_from_spec(spec)

        sys.modules["trainer"] = trainer_module
        sys.modules["__main__"] = trainer_module

    def _handle_local_notebook_trainer(self):
        notebook_path = f"/workspace/models/{self.model_name}/{self.model_version_id}/notebook.ipynb"  # noqa

        imports, trainer = notebook_utils.parse_notebook(notebook_path)
        trainer_source = notebook_utils.generate_trainer_from_template(
            model_name=self.model_name,
            imports=imports,
            trainer=trainer,
            model_version_id=self.model_version_id,
        )
        trainer_path = (
            f"/workspace/models/{self.model_name}/{self.model_version_id}/trainer.py"
        )

        with open(trainer_path, "w") as f_out:
            f_out.write(trainer_source)

        spec = importlib.util.spec_from_file_location("trainer", trainer_path)
        trainer_module = importlib.util.module_from_spec(spec)

        sys.modules["trainer"] = trainer_module
        sys.modules["__main__"] = trainer_module

    def save(
        self,
        *,
        model,
    ):
        """
        Save a model artifact to the slai backend
        """
        framework_name = self._get_framework_name(model)
        model_data = None

        if self.runtime == ValidRuntimes.Colab:
            self._handle_colab_trainer()
        elif self.runtime == ValidRuntimes.LocalNotebook:
            self._handle_local_notebook_trainer()

        # torch
        if framework_name == ValidModelFrameworks.Torch:
            model_data, requirements = ModelSaver.save_pytorch(model)
        elif framework_name in []:
            pass

        if model_data is None:
            raise UnsupportedModelFormat("invalid_model_format")

        model_artifact = self.model_client.create_model_artifact(
            model_data=model_data,
            artifact_type=framework_name,
            artifact_requirements=requirements,
            model_version_id=self.model_version_id,
        )
        return model_artifact
