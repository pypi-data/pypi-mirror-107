"""
The methods in this file help to compute aggregate values such as means on intervals.
They duplicate rows to replicate an interval for a value, for example to apply it to all
values +- 5%.
"""

import pandas as pd
from bisect import bisect


def convert_to_interval_on_values(table: pd.DataFrame, on_column: str, interval,
                                  values) -> pd.DataFrame:
    data = {c: [] for c in table.columns}
    for i, row in table.iterrows():
        lb, ub = interval(row[on_column])
        i_ = bisect(values, lb)
        for v in values[i_:]:
            if v > ub:
                break
            for c in table.columns:
                if c == on_column:
                    data[c].append(v)
                else:
                    data[c].append(row[c])
    return pd.DataFrame(data)


def convert_to_interval(table: pd.DataFrame, on_column: str, interval) -> pd.DataFrame:
    values = []
    for v in table[on_column].unique():
        lb, ub = interval(v)
        values.append(lb)
        values.append(ub)
    values.sort()

    return convert_to_interval_on_values(table, on_column, interval, values)


def convert_to_percentage_interval(table: pd.DataFrame, on_column: str, percentage):
    def interval(v):
        d = (percentage / 100) * v
        return v - d, v + d

    return convert_to_interval(table, on_column, interval)
