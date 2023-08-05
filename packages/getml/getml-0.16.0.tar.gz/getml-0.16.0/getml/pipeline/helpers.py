# Copyright 2021 The SQLNet Company GmbH

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to
# deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
# sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

"""
Collection of helper functions not intended to be used by the end-user.
"""

import random
import string
from copy import deepcopy

import numpy as np

from getml.data import DataFrame, Placeholder, roles
from getml.data.helpers import _is_typed_list, _remove_trailing_underscores
from getml.feature_learning import (
    FastPropModel,
    FastPropTimeSeries,
    MultirelModel,
    MultirelTimeSeries,
    RelboostModel,
    RelboostTimeSeries,
    RelMTModel,
    RelMTTimeSeries,
)

from getml.predictors import (
    LinearRegression,
    LogisticRegression,
    XGBoostClassifier,
    XGBoostRegressor,
)

from getml.preprocessors import (
    EmailDomain,
    Imputation,
    Mapping,
    Seasonal,
    Substring,
    TextFieldSplitter,
)

# --------------------------------------------------------------------


def _attach_empty(my_list, max_length, empty_val):
    assert len(my_list) <= max_length, "length exceeds max_length!"
    diff = max_length - len(my_list)
    return my_list + [empty_val] * diff


# --------------------------------------------------------------------


def _check_df_types(population_table, peripheral_tables):
    if not isinstance(population_table, DataFrame):
        raise TypeError("'population_table' must be a getml.data.DataFrame")

    if not _is_typed_list(peripheral_tables, DataFrame):
        raise TypeError(
            """'peripheral_tables' must be a getml.data.DataFrame
                          or a list of those"""
        )


# --------------------------------------------------------------------


def _extract_df_by_name(df_dict, name):
    """
    Extracts a data frame signified by name from df_dict.
    """

    if name not in df_dict:
        raise ValueError(
            """The dictionary you passed contains no key
               called '"""
            + name
            + "'."
        )

    if not isinstance(df_dict[name], DataFrame):
        raise TypeError("'" + name + "' must be a getml.data.DataFrame.")

    return df_dict[name]


# --------------------------------------------------------------------


def _extract_dfs(df_dict, placeholders):
    """
    Transforms df_dict into a list of data frames
    corresponding to the placeholders.
    """
    if not _is_typed_list(placeholders, Placeholder):
        raise TypeError("'placeholders' must be a list of Placeholders")
    return [_extract_df_by_name(df_dict, elem.name) for elem in placeholders]


# --------------------------------------------------------------------


def _infer_peripheral(population):
    def _get_names(population):
        return [p.name for p in population.joined_tables] + [
            name for p in population.joined_tables for name in _get_names(p)
        ]

    names = _get_names(population)
    names = np.unique(names)
    np.sort(names)
    return [Placeholder(name) for name in names.tolist()]


# --------------------------------------------------------------------


def _make_id():
    letters = string.ascii_letters + string.digits
    return "".join([random.choice(letters) for _ in range(6)])


# --------------------------------------------------------------------


def _parse_fe(some_dict):
    kwargs = _remove_trailing_underscores(some_dict)

    fe_type = kwargs["type"]

    del kwargs["type"]

    if "propositionalization" in kwargs:
        kwargs["propositionalization"] = _parse_fe(kwargs["propositionalization"])

    if fe_type == "FastPropModel":
        return FastPropModel(**kwargs)

    if fe_type == "FastPropTimeSeries":
        return FastPropTimeSeries(**kwargs)

    if fe_type == "MultirelModel":
        return MultirelModel(**kwargs)

    if fe_type == "MultirelTimeSeries":
        return MultirelTimeSeries(**kwargs)

    if fe_type == "RelboostModel":
        return RelboostModel(**kwargs)

    if fe_type == "RelboostTimeSeries":
        return RelboostTimeSeries(**kwargs)

    if fe_type == "RelMTModel":
        return RelMTModel(**kwargs)

    if fe_type == "RelMTTimeSeries":
        return RelMTTimeSeries(**kwargs)

    raise ValueError("Unknown feature learning algorithm: " + fe_type)


# --------------------------------------------------------------------


def _parse_pred(some_dict):

    kwargs = _remove_trailing_underscores(some_dict)

    pred_type = kwargs["type"]

    del kwargs["type"]

    if pred_type == "LinearRegression":
        return LinearRegression(**kwargs)

    if pred_type == "LogisticRegression":
        return LogisticRegression(**kwargs)

    if pred_type == "XGBoostClassifier":
        return XGBoostClassifier(**kwargs)

    if pred_type == "XGBoostRegressor":
        return XGBoostRegressor(**kwargs)

    raise ValueError("Unknown predictor: " + pred_type)


# --------------------------------------------------------------------


def _parse_preprocessor(some_dict):
    kwargs = _remove_trailing_underscores(some_dict)

    pre_type = kwargs["type"]

    del kwargs["type"]

    if pre_type == "EmailDomain":
        return EmailDomain()

    if pre_type == "Imputation":
        return Imputation(**kwargs)

    if pre_type == "Mapping":
        return Mapping(**kwargs)

    if pre_type == "Seasonal":
        return Seasonal()

    if pre_type == "Substring":
        return Substring(**kwargs)

    if pre_type == "TextFieldSplitter":
        return TextFieldSplitter()

    raise ValueError("Unknown preprocessor: " + pre_type)


# --------------------------------------------------------------------


def _print_time_taken(begin, end, msg):
    """Prints time required to fit a model.

    Args:
        begin (float): :func:`time.time` output marking the beginning
            of the training.
        end (float): :func:`time.time` output marking the end of the
            training.
        msg (str): Message to display along the duration.

    Raises:
        TypeError: If any of the input is not of proper type.

    """

    # ----------------------------------------------------------------

    if not isinstance(begin, float):
        raise TypeError("'begin' must be a float as returned by time.time().")

    if not isinstance(end, float):
        raise TypeError("'end' must be a float as returned by time.time().")

    if not isinstance(msg, str):
        raise TypeError("'msg' must be a str.")

    # ----------------------------------------------------------------

    seconds = end - begin

    hours = int(seconds / 3600)
    seconds -= float(hours * 3600)

    minutes = int(seconds / 60)
    seconds -= float(minutes * 60)

    seconds = round(seconds, 6)

    print(msg + str(hours) + "h:" + str(minutes) + "m:" + str(seconds))

    print("")


# --------------------------------------------------------------------


def _replace_with_nan_maybe(dict_):
    dict_ = deepcopy(dict_)

    for key, values in dict_.items():
        if isinstance(values, list):
            dict_[key] = [np.nan if value == -1 else value for value in values]

    return dict_


# --------------------------------------------------------------------


def _set_unused(data_frame, keep_columns, table, marker):

    assert isinstance(data_frame, DataFrame), "Wrong type"
    assert isinstance(table, str) or table is None, "Wrong type"
    assert marker in ("[POPULATION]", "[PERIPHERAL]"), "Unknown marker"

    keep_colnames = [
        desc["name_"]
        for desc in keep_columns
        if (desc["table_"] == table and desc["marker_"] == marker)
        or (marker == "[POPULATION]" and desc["marker_"] == "[POPULATION]")
    ]

    data_frame.refresh()

    categorical = [
        col for col in data_frame.categorical_names if col not in keep_colnames
    ]

    numerical = [col for col in data_frame.numerical_names if col not in keep_colnames]

    text = [col for col in data_frame.text_names if col not in keep_colnames]

    if categorical:
        data_frame.set_role(categorical, roles.unused_string)

    if numerical:
        data_frame.set_role(numerical, roles.unused_float)

    if text:
        data_frame.set_role(text, roles.unused_string)


# --------------------------------------------------------------------


def _transform_peripheral(peripheral_tables, placeholders):
    """
    Transforms the peripheral_tables into the desired list
    format
    """
    peripheral_tables = peripheral_tables or []

    if isinstance(peripheral_tables, dict):
        peripheral_tables = _extract_dfs(peripheral_tables, placeholders)

    if isinstance(peripheral_tables, DataFrame):
        peripheral_tables = [peripheral_tables]

    return peripheral_tables


# --------------------------------------------------------------------


def _unlist_maybe(list_):
    """
    `_unlist_maybe` has a unstable return type and should therefore only
    be used in interactive contexts. An example are a pipeline's atomic scores
    properties (auc, accuracy, ...) that are just convenience wrappers for
    interactive sessions.
    """
    if len(list_) == 1:
        return list_[0]
    return list_


# ------------------------------------------------------------
