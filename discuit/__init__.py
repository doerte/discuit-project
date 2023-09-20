import logging
from .data import Output
from .run import run_all


logging.getLogger(__name__).addHandler(logging.NullHandler())

__all__ = ['run_all', 'Output']

__author__ = "Dörte de Kok"
__email__ = "me@doerte.eu"
__version__ = "0.4.1"
