import pickle
import sys
from pathlib import Path

import numpy as np
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


def save_numpy_array_data(file_path: str, array: np.array) -> None:
    """
    Save numpy array data to file
    file_path: str location of file to save
    array: np.array data to save.
    """
    try:
        dir_path = Path(file_path).parent
        dir_path.mkdir(parents=True, exist_ok=True)
        with Path(file_path).open("wb") as file_obj:
            np.save(file_obj, array)
    except Exception as e:
        raise NetworkSecurityException(e, sys) from e


def save_object(file_path: str, obj: object) -> None:
    try:
        logging.info("Entered the save_object method of MainUtils class")
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)
        with Path(file_path).open("wb") as file_obj:
            pickle.dump(obj, file_obj)
        logging.info("Exited the save_object method of MainUtils class")
    except Exception as e:
        raise NetworkSecurityException(e, sys) from e


def load_object(file_path: str) -> object:
    try:
        if not Path(file_path).exists():
            raise Exception(f"The file: {file_path} is not exists")
        with Path(file_path).open("rb") as file_obj:
            print(file_obj)
            return pickle.load(file_obj)
    except Exception as e:
        raise NetworkSecurityException(e, sys) from e


def load_numpy_array_data(file_path: str) -> np.array:
    """
    Load numpy array data from file
    file_path: str location of file to load
    return: np.array data loaded.
    """
    try:
        with Path(file_path).open("rb") as file_obj:
            return np.load(file_obj)
    except Exception as e:
        raise NetworkSecurityException(e, sys) from e

