import sys

from network_security.exception.exception import NetworkSecurityException


class NetworkModel:
    def __init__(self, preprocessor: object, model: object) -> None:
        try:
            self.preprocessor = preprocessor
            self.model = model
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def predict(self, x: object) -> object:
        try:
            x_transform = self.preprocessor.transform(x)
            y_hat = self.model.predict(x_transform)
            return y_hat
        except Exception as e:
            raise NetworkSecurityException(e, sys)
