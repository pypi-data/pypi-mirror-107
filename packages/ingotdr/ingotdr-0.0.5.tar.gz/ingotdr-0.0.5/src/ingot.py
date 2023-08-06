import random
import pulp as pl
import numpy as np
from sklearn.base import BaseEstimator, ClassifierMixin
import re
import pandas as pd


def atoi(text):
    """
        Based on a stackoverflow post:
        https://stackoverflow.com/questions/5967500/how-to-correctly-sort-a-string-with-a-number-inside
    """
    return int(text) if text.isdigit() else text


def natural_keys(text):
    '''
    alist.sort(key=natural_keys) sorts in human order
    http://nedbatchelder.com/blog/200712/human_sorting.html
    (See Toothy's implementation in the comments)
    '''
    return [atoi(c) for c in re.split(r'(\d+)', text)]


class INGOTClassifier(BaseEstimator, ClassifierMixin):
    """
    A class to represent INGOT-DR classifier
    """

    def __init__(self, w_weight=1, lambda_p=1, lambda_z=1, lambda_e=1, false_positive_rate_upper_bound=None,
                 false_negative_rate_upper_bound=None, max_rule_size=None, rounding_threshold=1e-5,
                 lp_relaxation=False, only_slack_lp_relaxation=False, lp_rounding_threshold=0,
                 is_it_noiseless=False, solver_name='PULP_CBC_CMD', solver_options=None):
        """
        Constructs all the necessary attributes for the classifier object.
        Parameters:
            w_weight (vector, float): A vector, float to provide prior weight. Default to vector of 1.
            lambda_p (float): Regularization coefficient for positive labels. Default to 1.
            lambda_z (float): Regularization coefficient for negative labels. Default to 1.
            lambda_e (float): Regularization coefficient for all slack variables. Default to 1.
            false_positive_rate_upper_bound (float): False positive rate(FPR) upper bound. Default to None.
            false_negative_rate_upper_bound (float): False negative rate(FNR) upper bound. Default to None.
            max_rule_size (int): Maximum rule size. Default to None.
            rounding_threshold (float): Threshold for ilp solutions for Rounding to 0 and 1. Default to 1e-5
            lp_relaxation (bool): A flag to use the lp relaxed version. Default to False.
            only_slack_lp_relaxation (bool): A flag to only use the lp relaxed slack variables. Default to False.
            lp_rounding_threshold (float): Threshold for lp solutions for Rounding to 0 and 1. Default to 0.
            Range from 0 to 1.
            is_it_noiseless (bool): A flag to specify whether the problem is noisy or noiseless. Default to False.
            solver_name (str): Solver's name provided by Pulp. Default to 'PULP_CBC_CMD'.
            solver_options (dic): Solver's options provided by Pulp. Default to None.
        """

        self.lambda_e = lambda_e
        self.lambda_p = lambda_p
        self.lambda_z = lambda_z
        try:
            assert isinstance(w_weight, (int, float, list))
            self.w_weight = w_weight
        except AssertionError:
            print("w_weight should be either int, float or list of numbers")
        self.false_positive_rate_upper_bound = false_positive_rate_upper_bound
        self.false_negative_rate_upper_bound = false_negative_rate_upper_bound
        self.max_rule_size = max_rule_size
        self.rounding_threshold = rounding_threshold
        self.lp_relaxation = lp_relaxation
        self.only_slack_lp_relaxation = only_slack_lp_relaxation
        self.lp_rounding_threshold = lp_rounding_threshold
        self.is_it_noiseless = is_it_noiseless
        self.solver_name = solver_name
        self.solver_options = solver_options
        self.prob_ = None
        self.features_names = None

    def fit(self, A, label):
        """
        Function to fit the model with respect to the given data.

        Parameters:
            A (binary numpy 2d-array): The feature matrix.
            label (binary numpy array): The vector of labels.
        Returns:
            self (GroupTestingDecoder): A INGOTClassifier object including the solution
        """
        m, n = A.shape
        alpha = list(A.sum(axis=1))
        if isinstance(label, (pd.core.frame.DataFrame, pd.core.series.Series)):
            label = np.array(label).ravel()
        else:
            label = np.array(label)
        if isinstance(A, (pd.core.frame.DataFrame, pd.core.series.Series)):
            self.features_names = A.columns
            A = A.values.tolist()
        positive_label = np.where(label == 1)[0]
        negative_label = np.where(label == 0)[0]
        # -------------------------------------
        # Checking length of w_weight
        try:
            if isinstance(self.w_weight, list):
                assert len(self.w_weight) == n
        except AssertionError:
            print("length of w_weight should be equal to number of features")
        # -------------------------------------
        # Initializing the ILP problem
        p = pl.LpProblem('INGOTClassifier', pl.LpMinimize)

        # Variables kind
        if self.lp_relaxation:
            wVarCategory = 'Continuous'
        else:
            wVarCategory = 'Binary'
        # Variable w
        w = pl.LpVariable.dicts('w', range(n), lowBound=0, upBound=1, cat=wVarCategory)
        # --------------------------------------
        # Noiseless setting
        if self.is_it_noiseless:
            # Defining the objective function
            p += pl.lpSum([self.w_weight * w[i] if isinstance(self.w_weight, (int, float)) else self.w_weight[i] * w[i]
                           for i in range(n)])
            # Constraints
            for i in positive_label:
                p += pl.lpSum([A[i][j] * w[j] for j in range(n)]) >= 1
            for i in negative_label:
                p += pl.lpSum([A[i][j] * w[j] for j in range(n)]) == 0
        # --------------------------------------
        # Noisy setting
        else:
            if self.lp_relaxation or self.only_slack_lp_relaxation:
                en_upBound = None
                varCategory = 'Continuous'
            else:
                en_upBound = 1
                varCategory = 'Binary'
            # Variable ep
            if len(positive_label) != 0:
                ep = pl.LpVariable.dicts(name='ep', indexs=list(positive_label), lowBound=0, upBound=1, cat=varCategory)
            else:
                ep = []
            # Variable en
            if len(negative_label) != 0:
                en = pl.LpVariable.dicts(name='en', indexs=list(negative_label), lowBound=0, upBound=en_upBound,
                                         cat=varCategory)
            else:
                en = []
            # Defining the objective function
            p += pl.lpSum([self.w_weight * w[i] if isinstance(self.w_weight, (int, float)) else self.w_weight[i] * w[i]
                           for i in range(n)]) + \
                 pl.lpSum([self.lambda_e * self.lambda_p * ep[j] for j in positive_label]) + \
                 pl.lpSum([self.lambda_e * self.lambda_z * en[k] for k in negative_label])
            # Constraints
            for i in positive_label:
                p += pl.lpSum([A[i][j] * w[j] for j in range(n)] + ep[i]) >= 1
            for i in negative_label:
                if varCategory == 'Continuous':
                    p += pl.lpSum([A[i][j] * w[j] for j in range(n)] + -1 * en[i]) == 0
                else:
                    p += pl.lpSum([-1 * A[i][j] * w[j] for j in range(n)] + alpha[i] * en[i]) >= 0
            # Additional constraints
            if self.max_rule_size is not None:
                assert not self.lp_relaxation, "Can not set a maximum rule size (max_rule_size) if 'lp_relaxation' is" \
                                               " Ture! Set 'lp_relaxation' to False or 'max_rule_size' to None."
                p += pl.lpSum([w[i] for i in range(n)]) <= self.max_rule_size
            if self.false_negative_rate_upper_bound is not None and len(ep) != 0:
                assert not self.lp_relaxation, "Can not set false negative rate upper bound (" \
                                               "false_negative_rate_upper_bound) if 'lp_relaxation' is " \
                                               "Ture! Set 'lp_relaxation' to False or " \
                                               "'false_negative_rate_upper_bound' to None. "
                assert not self.only_slack_lp_relaxation, "Can not set false negative rate upper bound (" \
                                                          "false_negative_rate_upper_bound) if " \
                                                          "'only_slack_lp_relaxation' is " \
                                                          "Ture! Set 'only_slack_lp_relaxation' to False or " \
                                                          "'false_negative_rate_upper_bound' to None. "
                p += pl.lpSum(ep) <= self.false_negative_rate_upper_bound * len(positive_label)
            if self.false_positive_rate_upper_bound is not None and len(en) != 0:
                assert not self.lp_relaxation, "Can not set false positive rate upper bound (" \
                                               "false_positive_rate_upper_bound) if 'lp_relaxation' is " \
                                               "Ture! Set 'lp_relaxation' to False or " \
                                               "'false_positive_rate_upper_bound' to None. "
                assert not self.only_slack_lp_relaxation, "Can not set false positive rate upper bound (" \
                                                          "false_positive_rate_upper_bound) if " \
                                                          "'only_slack_lp_relaxation' is " \
                                                          "Ture! Set 'only_slack_lp_relaxation' to False or " \
                                                          "'false_positive_rate_upper_bound' to None. "
                p += pl.lpSum(en) <= self.false_positive_rate_upper_bound * len(negative_label)

        if self.solver_options is not None:
            solver = pl.get_solver(self.solver_name, **self.solver_options)
        else:
            solver = pl.get_solver(self.solver_name)
        p.solve(solver)
        if not self.lp_relaxation:
            p.roundSolution(epsInt=self.rounding_threshold)
        # ----------------
        self.prob_ = p
        # print("Status:", pl.LpStatus[p.status])
        return self

    def get_params_dictionary(self, variable_type='w'):
        """
        Function to provide a dictionary of individuals with their status obtained by decoder.
        Parameters:
            self (INGOTClassifier): Classifier object.
            variable_type (str): Type of the variable.e.g. 'w','ep' or 'en'
        Returns:
            w_solutions_dict (dict): A dictionary of features with their values in the model.
        """
        assert pl.LpStatus[self.prob_.status] != 'Infeasible', "Problem is {}! Set 'is_it_noiseless'" \
                                                               " argument to False. If there is still a problem you " \
                                                               "should relax/change some of additional constraints." \
                                                               "".format(pl.LpStatus[self.prob_.status])
        try:
            assert self.prob_ is not None
            # for v in self.prob_.variables() if variable_type in v.name and v.varValue > 0])
            # Pulp uses ASCII sort when we recover the solution. It would cause a lot of problems when we want
            # to use the solution. We need to use alphabetical sort based on variables names (v.names). To do so
            # we use natural_keys function and the following lines of codes
            w_solution_dict = dict([(v.name, v.varValue)
                                    for v in self.prob_.variables() if variable_type in v.name])
            index_map = {v: i for i, v in enumerate(sorted(w_solution_dict.keys(), key=natural_keys))}
            w_solution_dict = {k: v for k, v in sorted(w_solution_dict.items(), key=lambda pair: index_map[pair[0]])}
        except AttributeError:
            raise RuntimeError("You must fit the data first!")
        return w_solution_dict

    def solution(self):
        """
        Function to provide a vector of features importance.
        Parameters:
            self (INGOTClassifier): Classifier object.
        Returns:
            w_solutions (vector): A vector of features importance.
        """
        assert pl.LpStatus[self.prob_.status] != 'Infeasible', "Problem is {}! Set 'is_it_noiseless'" \
                                                               " argument to False. If there is still a problem you " \
                                                               "should relax/change some of additional constraints." \
                                                               "".format(pl.LpStatus[self.prob_.status])
        try:
            assert self.prob_ is not None
            # Pulp uses ASCII sort when we recover the solution. It would cause a lot of problems when we want
            # to use the solution. We need to use alphabetical sort based on variables names (v.names). To do so
            # we use natural_keys function and the following lines of codes
            w_solution = self.get_params_dictionary(variable_type='w')
            index_map = {v: i for i, v in enumerate(sorted(w_solution.keys(), key=natural_keys))}
            w_solution = [v for k, v in sorted(w_solution.items(), key=lambda pair: index_map[pair[0]])]
            if self.lp_relaxation:
                w_solution = [1 if i > self.lp_rounding_threshold else 0 for i in w_solution]
        except AttributeError:
            raise RuntimeError("You must fit the data first!")
        return w_solution

    def predict(self, A):
        """
        Function to predict test results based on solution.
        Parameters:
            self (INGOTClassifier): Classifier object.
            A (binary numpy 2d-array): The feature array or matrix.
        Returns:
             A vector of predicted labels.
        """
        assert pl.LpStatus[self.prob_.status] != 'Infeasible', "Problem is {}! Set 'is_it_noiseless'" \
                                                               " argument to False. If there is still a problem you " \
                                                               "should relax/change some of additional constraints." \
                                                               "".format(pl.LpStatus[self.prob_.status])
        if isinstance(A, (pd.core.frame.DataFrame, pd.core.series.Series)):
            A = A.values.tolist()
        return np.minimum(np.matmul(A, self.solution()), 1)

    def learned_rule(self, return_type='feature_name'):
        """
        Return a list of rules

        Parameters:
            return_type (str): Type of the return list. It could be list of name of features of their ids in the
            feature matrix. Acceptable values are 'feature_name' or 'feature_id'. Default to 'feature_name'.

        Return:
            return (vector): A vector of learned rule.
        """
        sol = self.solution()
        if self.features_names is not None and return_type == 'feature_name':
            return [self.features_names[idx] for idx, i in enumerate(sol) if i > self.rounding_threshold]
        else:
            return [idx for idx, i in enumerate(sol) if i > self.rounding_threshold]

    def write(self, fileType='mps', **kwargs):
        """
        Create a file from the problem
        Parameters:
            fileType (str): Type of the file. Possible choices: mps, lp, json, display. Default to mps.
            kwargs (dict): additional keyword arguments for pulp writing functions. i.e writeMPS, writeLP, toJson.
        Returns:
            None
        """
        if fileType.lower() == 'mps':
            self.prob_.writeMPS(**kwargs)
        elif fileType.lower() == 'lp':
            self.prob_.writeLP(**kwargs)
        elif fileType.lower() == 'json':
            self.prob_.toJson(**kwargs)
        elif fileType.lower() == 'display':
            print(self.prob_)
        else:
            print('fileType should be either "mps", "lp", "json" or "display". "display would print the problem on'
                  ' the screen."')
