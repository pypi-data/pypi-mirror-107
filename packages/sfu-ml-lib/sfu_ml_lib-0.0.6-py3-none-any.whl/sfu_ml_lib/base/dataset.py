import typing
from abc import ABC, abstractmethod
from typing import Tuple, Optional, Iterator, TypeVar, Union

import numpy as np
import tensorflow as tf
from tensorflow import Tensor


T = TypeVar('T')
TensorType = Union[np.ndarray, Tensor]
TensorTuple = Union[TensorType, Tuple[TensorType, ...]]
BatchType = Union[
    Tuple[TensorTuple, None],
    Tuple[TensorTuple, TensorTuple],
    Tuple[TensorTuple, TensorTuple, TensorType],
]
DatasetType = Union[Iterator[BatchType], tf.data.Dataset]


class Dataset(ABC):
    size: int
    targets: Optional[TensorType] = None

    @abstractmethod
    @typing.no_type_check
    def get_batches(self, *args) -> DatasetType:
        ...

    @abstractmethod
    def subset(self: T, indices: TensorType) -> T:
        ...
