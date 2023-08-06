from .core import (Dense, BackendType, ConvolutionMode, PoolingType,
                   LearningType, LayerType, TensorType, HwVersion, NP,
                   NPMapping, NPSpace, MeshMapper, Layer, Device, devices,
                   NSoC_v1, NSoC_v2, Logger, __version__)

from .layer import *
from .input_data import InputData
from .fully_connected import FullyConnected
from .convolutional import Convolutional
from .separable_convolutional import SeparableConvolutional
from .input_convolutional import InputConvolutional
from .concat import Concat
from .model import Model
from .statistics import LayerStatistics, SequenceStatistics
from .np import *

Layer.__repr__ = layer_repr
Layer.set_variable = set_variable
Layer.get_variable = get_variable
Layer.get_variable_names = get_variable_names
Layer.get_learning_histogram = get_learning_histogram

NP.Info.__repr__ = np_info_repr
NP.Mesh.__repr__ = np_mesh_repr
