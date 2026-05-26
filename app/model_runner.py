from abc import ABC, abstractmethod


class ModelRunner(ABC):
    @abstractmethod
    def predict(self, input: str) -> str:
        raise NotImplementedError


class DummyModelRunner(ModelRunner):
    def predict(self, input: str) -> str:
        return input
