from typing import Dict

import subprocess

from .multiprocess_api import ModelDeploymentConfig


def run_model_fleet(model_deployments: Dict[str, ModelDeploymentConfig]):
    for model_config in model_deployments.values():
        model_class = model_config.model_class
        for worker in range(len(model_config.allocations)):
            subprocess.Popen([
                'python', '-m', 'fastformers.run_server',
                '--model', "{0}.{1}".format(model_class.__module__, model_class.__name__),
                '--path', model_config.path,
                '--device', str(model_config.allocations[worker]),
                '--port', str(model_config.port + worker),
                f'--{"" if model_config.use_torchscript else "no-"}torchscript']
            )
