from slai.loaders.torch_loader import TorchLoader
from slai.modules.model_saver import ValidModelFrameworks
from slai.exceptions import UnsupportedModelFormat


class ModelLoader:
    @classmethod
    def load_model(cls, *, model_artifact, deployment_instance_path, artifact_type):
        loaded_model = None

        if artifact_type == ValidModelFrameworks.Torch:
            loaded_model = TorchLoader.load_model(
                model_artifact=model_artifact,
                deployment_instance_path=deployment_instance_path,
            )
        else:
            raise UnsupportedModelFormat("invalid_artifact_type")

        return loaded_model
