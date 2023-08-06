from typing import Type, List

import os
import torch


class ModelDeploymentConfig:
    def __init__(
            self, model_class: Type[torch.nn.Module], path: str, port: int, allocations: List[int],
            use_torchscript: bool = True
    ):
        self.model_class = model_class
        self.port = port
        self.path = os.path.join('mnt', 'components', path)
        self.allocations = allocations
        self.use_torchscript = use_torchscript
