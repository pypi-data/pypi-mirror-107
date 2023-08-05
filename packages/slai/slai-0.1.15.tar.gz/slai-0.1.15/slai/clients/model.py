from slai.clients.project import get_project_client
from slai.clients.cli import get_cli_client
from slai.modules.parameters import from_config
from importlib import import_module


def get_model_client(*, model_name, project_name):
    import_path = from_config(
        "MODEL_CLIENT",
        "slai.clients.model.ModelClient",
    )
    class_ = import_path.split(".")[-1]
    path = ".".join(import_path.split(".")[:-1])
    return getattr(import_module(path), class_)(
        model_name=model_name, project_name=project_name
    )


class ModelClient:
    def __init__(self, *, model_name=None, project_name=None):
        self.project_client = get_project_client(project_name=project_name)
        self.cli_client = get_cli_client()

        self.model_name = model_name
        self.model = self.get_model()

    def get_project_name(self):
        return self.project_client.get_project_name()

    def create_model_artifact(
        self, *, model_data, artifact_type, artifact_requirements, model_version_id=None
    ):
        if model_version_id is None:
            model_version_id = self.model["model_version_id"]

        model_artifact = self.cli_client.create_model_artifact(
            model_version_id=model_version_id,
            model_data=model_data,
            artifact_type=artifact_type,
            artifact_requirements=artifact_requirements,
        )
        return model_artifact

    def create_model_deployment(
        self,
        *,
        model_artifact_id,
        model_handler_data,
        requirements,
    ):
        model_deployment = self.cli_client.create_model_deployment(
            model_artifact_id=model_artifact_id,
            model_handler_data=model_handler_data,
            requirements=requirements,
        )
        return model_deployment

    def update_model(self, *, key, value):
        model_data = self.get_model()
        model_data[key] = value
        model_data = self.cli_client.update_model(model_data=model_data)
        return model_data

    def get_model(self):
        model_data = self.cli_client.retrieve_model(
            project_name=self.project_client.get_project_name(),
            name=self.model_name,
        )
        return model_data

    def get_latest_model_artifact(self, model_version_id=None):
        model_data = self.get_model()

        if model_version_id is None:
            model_version_id = model_data["model_version_id"]

        model_artifact = self.cli_client.retrieve_model_artifact(
            model_version_id=model_version_id,
            model_artifact_id=None,
        )
        return model_artifact


class MockModelClient:
    def __init__(self, *, model_name, project_name):
        pass

    def get_project_name(self):
        return "MOCK_PROJECT_NAME"

    def create_model_artifact(
        self, *, model_data, artifact_type, artifact_requirements
    ):
        return {
            "id": "60329220dd191a68cfb474ec",
            "model_version_id": "60328ce6dd191a6608bb7da9",
            "artifact_type": artifact_type,
            "artifact_requirements": {"torch": "==1.70.0a0"},
            "created": "2021-02-21T12:02:24.503850",
        }

    def update_model(self, *, key, value):
        model_data = {
            "id": "60329220dd191a68cfb474ec",
            "project_name": "something",
            "project_id": "60328ce6dd191a6608bb7da9",
            "name": "something1",
            "notebook_uri": None,
            "model_version_id": "60329220dd191a68cfb474ed",
            "created": "2021-02-21T12:02:24.503850",
            "updated": "2021-02-21T12:02:24.635203",
        }
        model_data[key] = value
        return model_data

    def get_model(self):
        return {
            "id": "60329220dd191a68cfb474ec",
            "project_name": "something",
            "project_id": "60328ce6dd191a6608bb7da9",
            "name": "something1",
            "notebook_uri": None,
            "model_version_id": "60329220dd191a68cfb474ed",
            "created": "2021-02-21T12:02:24.503850",
            "updated": "2021-02-21T12:02:24.635203",
        }
