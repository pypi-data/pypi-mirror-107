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
Feature learning for time series based on relational boosting.
"""

from dataclasses import dataclass, field
from typing import List, Union

from .fastprop_model import FastPropModel
from .feature_learner import _FeatureLearner
from .loss_functions import SquareLoss
from .validation import (
    _validate_relboost_model_parameters,
    _validate_time_series_parameters,
)

# --------------------------------------------------------------------


@dataclass(repr=False)
class RelMTTimeSeries(_FeatureLearner):
    """Feature learning based on relational linear model trees.

    :class:`~getml.feature_learning.RelMTTimeSeries` automates feature learning
    for relational data and time series. It is based on a
    generalization of linear model trees to relational data, hence
    the name. A linear model tree is a decision tree
    with linear models on its leaves.

    Args:
        horizon (float, optional):

            The period of time you want to look ahead to generate the
            predictions.

        memory (float, optional):

            The period of time you want to the to look back until the
            algorithm "forgets" the data. If you set memory to 0.0, then
            there will be no limit.

        self_join_keys (List[str], optional):

            A list of the join keys to use for the self-join. If none are
            passed, then the self join will take place on the entire population
            table.

        ts_name (str, optional):

            The name of the time stamp column to be used. If none is passed,
            then the row ID will be used.

        allow_lagged_targets (bool, optional):

            In some time series problems, it is allowed to aggregate over
            target variables from the past. In others, this is not allowed.
            If *allow_lagged_targets* is set to True, you must pass a horizon
            that is greater than zero, otherwise you would have a data leak
            (an exception will be thrown to prevent this).

        allow_avg (bool, optional):

            Whether to allow an AVG aggregation. Particularly for time
            series problems, AVG aggregations are not necessary and you
            can save some time by taking them out.

        delta_t (float, optional):

            Frequency with which lag variables will be explored in a
            time series setting. When set to 0.0, there will be no lag
            variables.

            For more information, please refer to
            :ref:`data_model_time_series`. Range: [0, :math:`\\infty`]

        gamma (float, optional):

            During the training of RelMT, which is based on
            gradient tree boosting, this value serves as the minimum
            improvement in terms of the `loss_function` required for a
            split of the tree to be applied. Larger `gamma` will lead
            to fewer partitions of the tree and a more conservative
            algorithm. Range: [0, :math:`\\infty`]

        loss_function (:class:`~getml.feature_learning.loss_functions`, optional):

            Objective function used by the feature learning algorithm
            to optimize your features. For regression problems use
            :class:`~getml.feature_learning.loss_functions.SquareLoss` and for
            classification problems use
            :class:`~getml.feature_learning.loss_functions.CrossEntropyLoss`.

        max_depth (int, optional):

            Maximum depth of the trees generated during the gradient
            tree boosting. Deeper trees will result in more complex
            models and increase the risk of overfitting. Range: [0,
            :math:`\\infty`]

        min_df (int, optional):

            Only relevant for columns with role :const:`~getml.data.roles.text`.
            The minimum
            number of fields (i.e. rows) in :const:`~getml.data.roles.text` column a
            given word is required to appear in to be included in the bag of words.
            Range: [1, :math:`\\infty`]

        min_num_samples (int, optional):

            Determines the minimum number of samples a subcondition
            should apply to in order for it to be considered. Higher
            values lead to less complex statements and less danger of
            overfitting. Range: [1, :math:`\\infty`]

        num_features (int, optional):

            Number of features generated by the feature learning
            algorithm. Range: [1, :math:`\\infty`]

        num_subfeatures (int, optional):

            The number of subfeatures you would like to extract in a
            subensemble (for snowflake data model only). See
            :ref:`data_model_snowflake_schema` for more
            information. Range: [1, :math:`\\infty`]

        num_threads (int, optional):

            Number of threads used by the feature learning algorithm. If set to
            zero or a negative value, the number of threads will be
            determined automatically by the getML engine. Range:
            [-:math:`\\infty`, :math:`\\infty`]

        propositionalization (:class:`~getml.feature_learning.FastPropModel`, optional):

            The feature learner used for joins, which are flagged to be
            propositionalized (through setting a join's `relationship` parameter to
            :const:`getml.data.relationship.propositionalization`)

        reg_lambda (float, optional):

            L2 regularization on the weights in the gradient boosting
            routine. This is one of the most important hyperparameters
            in the :class:`~getml.feature_learning.RelMTTimeSeries` as it allows
            for the most direct regularization. Larger values will
            make the resulting model more conservative. Range: [0,
            :math:`\\infty`]

        sampling_factor (float, optional):

            RelMT uses a bootstrapping procedure (sampling with
            replacement) to train each of the features. The sampling
            factor is proportional to the share of the samples
            randomly drawn from the population table every time
            RelMT generates a new feature. A lower sampling factor
            (but still greater than 0.0), will lead to less danger of
            overfitting, less complex statements and faster
            training. When set to 1.0, roughly 20,000 samples are drawn
            from the population table. If the population table
            contains less than 20,000 samples, it will use standard
            bagging. When set to 0.0, there will be no sampling at
            all. Range: [0, :math:`\\infty`]

        seed (Union[int,None], optional):

            Seed used for the random number generator that underlies
            the sampling procedure to make the calculation
            reproducible. Internally, a `seed` of None will be mapped to
            5543. Range: [0, :math:`\\infty`]

        shrinkage (float, optional):

            Since RelMT works using a gradient-boosting-like
            algorithm, `shrinkage` (or learning rate) scales down the
            weights and thus the impact of each new tree. This gives
            more room for future ones to improve the overall
            performance of the model in this greedy algorithm. It must
            be between 0.0 and 1.0 with higher values leading to more
            danger of overfitting. Range: [0, 1]

        silent (bool, optional):

            Controls the logging during training.

        use_timestamps (bool, optional):

            Whether you want to ignore all elements in the peripheral
            tables where the time stamp is greater than the one in the
            corresponding elements of the population table. In other
            words, this determines whether you want add the condition

            .. code-block:: sql

                t2.time_stamp <= t1.time_stamp

            at the very end of each feature. It is strongly recommend
            to enable this behavior.

        vocab_size (int, optional):

            Determines the maximum number
            of words that are extracted in total from :const:`getml.data.roles.text`
            columns. This can be interpreted as the maximum size of the bag of words.
            Range: [0, :math:`\\infty`]


    Example:

        .. code-block:: python

            # Our forecast horizon is 0.
            # We do not predict the future, instead we infer
            # the present state from current and past sensor data.
            horizon = 0.0

            # We do not allow the time series features
            # to use target values from the past.
            # (Otherwise, we would need the horizon to
            # be greater than 0.0).
            allow_lagged_targets = False

            # We want our time series features to only use
            # data from the last 15 minutes
            memory = getml.data.time.minutes(15)

            feature_learner = getml.feature_learning.RelMTTimeSeries(
                    ts_name="date",
                    horizon=horizon,
                    memory=memory,
                    allow_lagged_targets=allow_lagged_targets,
                    num_features=30,
                    loss_function=getml.feature_learning.loss_functions.CrossEntropyLoss
            )

            predictor = getml.predictors.XGBoostClassifier(reg_lambda=500)

            pipe = getml.pipeline.Pipeline(
                tags=["memory=15", "no ts_name", "relmt"],
                feature_learners=[feature_learner],
                predictors=[predictor]
            )

            pipe.check(data_train)

            pipe = pipe.fit(data_train)

            predictions = pipe.predict(data_test)

            scores = pipe.score(data_test)
    """

    # ----------------------------------------------------------------

    allow_avg: bool = True
    delta_t: float = 0.0
    gamma: float = 0.0
    loss_function: str = SquareLoss
    max_depth: int = 2
    min_df: int = 30
    min_num_samples: int = 1
    num_features: int = 30
    num_subfeatures: int = 30
    num_threads: int = 0
    propositionalization: FastPropModel = FastPropModel()
    reg_lambda: float = 0.0
    sampling_factor: float = 1.0
    seed: int = 5543
    shrinkage: float = 0.1
    silent: bool = True
    use_timestamps: bool = True
    vocab_size: int = 500

    # ------------------------------------------------------------

    horizon: float = 0.0
    memory: float = 0.0
    self_join_keys: List[str] = field(default_factory=list)
    ts_name: str = ""
    allow_lagged_targets: bool = False

    # ------------------------------------------------------------

    def validate(self, params=None):
        """Checks both the types and the values of all instance
        variables and raises an exception if something is off.

        Args:
            params (dict, optional): A dictionary containing
                the parameters to validate. If not is passed,
                the own parameters will be validated.
        """

        # ------------------------------------------------------------

        if params is None:
            params = self.__dict__
        else:
            params = {**self.__dict__, **params}

        # ------------------------------------------------------------

        if not isinstance(params, dict):
            raise ValueError("params must be None or a dictionary!")

        # ------------------------------------------------------------

        if not isinstance(params["silent"], bool):
            raise TypeError("'silent' must be of type bool")

        # ------------------------------------------------------------

        for kkey in params:
            if kkey not in type(self)._supported_params:
                raise KeyError(
                    f"Instance variable '{kkey}' is not supported in {self.type}."
                )

        # ------------------------------------------------------------

        _validate_relboost_model_parameters(**params)

        # ------------------------------------------------------------

        _validate_time_series_parameters(**params)


# --------------------------------------------------------------------
