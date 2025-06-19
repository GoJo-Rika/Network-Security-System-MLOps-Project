import os

# import dill
import sys
from pathlib import Path

import yaml

from network_security.exception.exception import NetworkSecurityException
from network_security.logging.logger import logging


def read_yaml_file(file_path: str) -> dict:
    try:
        with Path(file_path).open("rb") as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise NetworkSecurityException(e, sys) from e


def write_yaml_file(file_path: str, content: object, replace: bool = False) -> None:
    try:
        if replace and Path(file_path).exists():
            Path(file_path).unlink()
        with Path(file_path).open("w") as file:
            yaml.dump(content, file)
            yaml.dump(content, file)
    except Exception as e:
        raise NetworkSecurityException(e, sys)
