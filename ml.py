#!/usr/bin/env python

import os
import subprocess
import logging
import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier, export_graphviz
from sklearn import preprocessing

class ML:
    def __init__(self, input_data):
        self._input_data = input_data
        self._logger = logging.getLogger(__name__)
        self.df = None

    def _encode_target(self, df, target_column):
        """Add column to df with integers for the target.

        Args
        ----
        df -- pandas DataFrame.
        target_column -- column to map to int, producing
                         new Target column.

        Returns
        -------
        df_mod -- modified DataFrame.
        targets -- list of target names.
        """
        df_mod = df.copy()
        targets = df_mod[target_column].unique()
        map_to_int = {name: n for n, name in enumerate(targets)}
        df_mod["target"] = df_mod[target_column].replace(map_to_int)

        return (df_mod, targets)

    def _encode_column(self, df, column):
        le = preprocessing.LabelEncoder()
        items = df[column].unique()
        le.fit(df[column])
        labels = le.transform(items)
        labels_map = {}
        for c in range(0, len(labels)):
            labels_map[items[c]] = labels[c]
        df[column] = df[column].replace(labels_map)
        return df

    def _visualize_tree(self, tree, feature_names):
        """Create tree png using graphviz.

        Args
        ----
        tree -- scikit-learn DecsisionTree.
        feature_names -- list of feature names.
        """
        with open("dt.dot", 'w') as f:
            export_graphviz(tree, out_file=f, feature_names=feature_names)

        command = ["dot", "-Tpng", "dt.dot", "-o", "dt.png"]
        try:
            subprocess.check_call(command)
        except:
            exit("Could not run dot, ie graphviz, to produce visualization")

    def create_dataframe(self):
        self.df = pd.DataFrame(self._input_data)
        self.df = self.df.dropna() # NaN must be dropped
        self._logger.debug("\n" + str(self.df))

    def decission_tree(self):
        df_mod, targets = self._encode_target(self.df, "departure_delay")
        features = list(df_mod.loc[:, df_mod.columns != 'departure_delay'])
        df_mod = self._encode_column(df_mod, "arrival_datetime")
        df_mod = self._encode_column(df_mod, "arrival_line")
        df_mod = self._encode_column(df_mod, "departure_datetime")
        df_mod = self._encode_column(df_mod, "departure_line")
        df_mod = self._encode_column(df_mod, "direction")
        df_mod = self._encode_column(df_mod, "vehicle_type")
        df_mod = self._encode_column(df_mod, "stop")
        print("features ", features)
        df_validation = df_mod[:1000]
        df_mod = df_mod[1000:]
        y = df_mod["target"]
        X = df_mod[features]
        dt = DecisionTreeClassifier(min_samples_split=20, random_state=99)
        dt.fit(X, y)
        #self._visualize_tree(dt, features)
        #probability = dt.predict_proba(df_mod.loc[:, df_mod.columns != "departure_delay"])
        prediction = dt.predict(df_validation.loc[:, df_mod.columns != "departure_delay"])
        import sys
        np.set_printoptions(threshold=sys.maxsize)
        print(prediction)
        true_positive = 0
        false_positive = 0
        true_negative = 0
        false_negative = 0
        skipped = 0
        for index, p in enumerate(prediction):
            try:
                print(df_validation["has_departure_delay"][df_validation.index == index])
                if df_validation["has_departure_delay"][df_validation.index == index].values[0] == (p > 60.0):
                    if df_validation["has_departure_delay"][df_validation.index == index].values[0]:
                        true_positive += 1
                    else:
                        true_negative += 1

                if df_validation["has_departure_delay"][df_validation.index == index].values[0] and (p < 60.0):
                    false_negative += 1

                if not df_validation["has_departure_delay"][df_validation.index == index].values[0] and (p > 60.0):
                    false_positive += 1
            except:
                skipped += 1
        print("TP (%): {}".format(true_positive/(1000 - skipped) * 100),
              "FP (%): {}".format(false_positive/(1000 - skipped) * 100),
              "TN (%): {}".format(true_negative/(1000 - skipped) * 100),
              "FN (%): {}".format(false_negative/(1000 - skipped) * 100),
              "SKIPPED: {}".format(skipped),
              sep="\n")
