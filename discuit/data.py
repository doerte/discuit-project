from dataclasses import dataclass
from dataclasses import field
from typing import List
from typing import Optional
import pandas as pd


@dataclass
class Result:
    identifier: str
    test: str
    feature: str
    df: float
    x2: float
    p: float


@dataclass
class Table:
    feature: str
    crosstab: Optional[pd.crosstab] = None


@dataclass
class Average:
    feature: str
    set_no: int
    mean: float


@dataclass
class Run:
    no_it: int
    significant: bool
    result: List[Result]
    tables: List[Table]
    dataframe: pd.DataFrame
    csv_name: str
    averages: List[Average]
    filename: str
    txt_name: Optional[str] = None



@dataclass
class Output:
    runs: List[Run] = field(default_factory=list)
