from __future__ import annotations

from typing import Any, Dict, Iterable, Optional, Type

import torch
from sklearn.base import BaseEstimator, ClassifierMixin
from skorch import NeuralNetClassifier
from torch import nn


class SkorchWrapper(ClassifierMixin, BaseEstimator):
    def __init__(
        self,
        module: Type[nn.Module],
        batch_size: int = 64,
        max_epochs: int = 5,
        learn_rate: float = 1e-3,
        device: str = "cuda",
        model_kwargs: Dict[str, Any] = None,
        optimizer: Type[torch.optim.Optimizer] = torch.optim.Adam,
    ):
        self.module = module
        self.device = device
        self.batch_size = batch_size
        self.max_epochs = max_epochs
        self.learn_rate = learn_rate
        self.model_kwargs = model_kwargs or {}
        self.wrapped_model: Optional[NeuralNetClassifier] = None
        self.optimizer = optimizer

    def fit(self, x: Any, y: Iterable[Any], **fit_kwargs: Any) -> SkorchWrapper:
        if self.wrapped_model is None:
            classes = set(y)
            n_classes = len(classes)
            self.model_kwargs["module__n_classes"] = n_classes
            self.wrapped_model = NeuralNetClassifier(
                module=self.module,
                device=self.device,
                batch_size=self.batch_size,
                max_epochs=self.max_epochs,
                lr=self.learn_rate,
                optimizer=self.optimizer,
                classes=classes,  # this is why we wrap - no point in pre-setting
                **self.model_kwargs
            )
        self.wrapped_model.fit(x, y, **fit_kwargs)
        return self

    def predict(self, x: Any) -> Any:
        if self.wrapped_model is None:
            raise ValueError("model was not fitted")
        return self.wrapped_model.predict(x)
