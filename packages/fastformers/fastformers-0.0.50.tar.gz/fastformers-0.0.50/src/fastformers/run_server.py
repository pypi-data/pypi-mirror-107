from typing import Type

import argparse
import torch
import importlib

from .multiprocess_api import ModelServer


def init_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', type=str, required=True)
    parser.add_argument('--path', type=str, required=True)
    parser.add_argument('--port', type=int, required=True)
    parser.add_argument('--device', type=int, required=True)
    parser.add_argument('--torchscript', dest='torchscript', action='store_true')
    parser.add_argument('--no-torchscript', dest='torchscript', action='store_false')
    return parser


def run_server():
    args = init_parser().parse_args()

    split_model_name = args.model.split('.')
    module_name = '.'.join(split_model_name[:-1])
    class_name = split_model_name[-1]

    port: int = args.port
    device = f'cuda:{args.device}'
    model_class: Type[torch.nn.Module] = getattr(importlib.import_module(module_name), class_name)
    model = model_class.from_pretrained(args.path).to(device)
    if args.torchscript:
        model = torch.jit.script(model)
    server = ModelServer(port=port, model=model, model_name=class_name)
    try:
        server.run()
    finally:
        server.close()


if __name__ == '__main__':
    run_server()
