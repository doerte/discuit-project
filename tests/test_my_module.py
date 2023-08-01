"""Tests for the discuit.my_module module.
"""
# import pytest

import pandas as pd
from discuit.clustering import prepare_data

d = {'keep': {0: 1.0, 1: 2.0, 2: 3.0}, 'drop': {0: 1.0, 1: 2.0, 2: 3.0}}
df = pd.DataFrame(d)

d_out = {"keep": {0: 1.0, 1: 2.0, 2: 3.0}}

def check_data():
    assert prepare_data([df],[],[],[],['drop']) == d_out
