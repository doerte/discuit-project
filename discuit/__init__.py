import logging
from .run import run_all


logging.getLogger(__name__).addHandler(logging.NullHandler())

__all__ = ['run_all']

__author__ = "Dörte de Kok"
__email__ = "me@doerte.eu"
__version__ = "0.1.0"
