from abc import ABC, abstractmethod
from dataclasses import dataclass

from sklearn.datasets import load_iris
from sklearn.neighbors import KNeighborsClassifier


@dataclass(frozen=True)
class IrisPrediction:
    class_id: int
    label: str


ModelInput = list[float]
ModelOutput = IrisPrediction


class ModelRunner(ABC):
    @abstractmethod
    def predict(self, features: ModelInput) -> ModelOutput:
        raise NotImplementedError


class IrisModelRunner(ModelRunner):
    def __init__(self) -> None:
        dataset = load_iris()
        self._target_names = [str(name) for name in dataset.target_names]
        self._model = KNeighborsClassifier(n_neighbors=3)
        self._model.fit(dataset.data, dataset.target)

    def predict(self, features: ModelInput) -> ModelOutput:
        class_id = int(self._model.predict([features])[0])
        return IrisPrediction(
            class_id=class_id,
            label=self._target_names[class_id],
        )
