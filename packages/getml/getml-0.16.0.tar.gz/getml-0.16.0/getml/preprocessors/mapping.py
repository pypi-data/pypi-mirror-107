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
Contains routines for preprocessing data frames.
"""

from getml.feature_learning.aggregations import mapping as mapping_aggregations

from .preprocessor import _Preprocessor


class Mapping(_Preprocessor):
    """
    A mapping preprocessor maps categorical values, discrete values and individual
    words in a text field to numerical values. These numerical values are retrieved
    by aggregating targets in the relational neighbourhood.

    You are particularly encouraged to use the mapping preprocessor in combination with
    :class:`~getml.feature_learning.FastPropModel` and
    :class:`~getml.feature_learning.FastPropTimeSeries`.

    Refer to the :ref:`User guide <mappings>` for more information.

    .. code-block:: python

        mapping = getml.preprocessors.Mapping()

        pipe = getml.pipeline.Pipeline(
            population=population_placeholder,
            peripheral=[order_placeholder, trans_placeholder],
            preprocessors=[mapping],
            feature_learners=[feature_learner_1, feature_learner_2],
            feature_selectors=feature_selector,
            predictors=predictor,
            share_selected_features=0.5
        )

    Args:
        aggregation (List[:class:`~getml.feature_learning.aggregations`], optional):

            The aggregation function to use over the targets.

            Must be from :mod:`~getml.feature_learning.aggregations`.

        min_freq (int, optional):

            The minimum number of targets required for a value to be included in
            the mapping. Range: [0, :math:`\\infty`]
    """

    # ----------------------------------------------------------------

    agg_sets = mapping_aggregations

    # ----------------------------------------------------------------

    def __init__(self, aggregation=None, min_freq=30):
        super().__init__()
        self.type = "Mapping"
        self.aggregation = aggregation or Mapping.agg_sets.Default
        self.min_freq = min_freq
