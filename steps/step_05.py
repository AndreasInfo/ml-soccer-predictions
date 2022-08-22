import datetime as dt
import pickle

import modules.features as feat
import modules.helper as helper
from sklearn.compose import ColumnTransformer
from sklearn.metrics import classification_report, make_scorer
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder


class ModelMaker:
    def __init__(self, df, num_features, cat_features, label, models, testrun):
        self.df = df
        self.num_features = num_features
        self.cat_features = cat_features
        self.label = label
        self.models = models
        self.testrun = testrun

    def do(self):
        print(f"Start: {dt.datetime.now()}")
        print()

        df_features = self.df.columns.tolist()
        features = self.num_features + self.cat_features
        features.append(self.label)
        print(f"Dropped features: {list(set(df_features) - set(features))}")

        self.df = self.df[features]

        for model in self.models:
            features = self.df.drop(self.label, axis=1)
            label = self.df[self.label]

            X_train = features
            y_train = label

            numeric_transformer = Pipeline(
                steps=[("scaling", None), ("binning", None), ("poly", None)]
            )

            categorical_transformer = Pipeline(
                steps=[("onehot", OneHotEncoder(sparse=False, handle_unknown="ignore"))]
            )

            preprocessor = ColumnTransformer(
                transformers=[
                    ("num", numeric_transformer, self.num_features),
                    ("cat", categorical_transformer, self.cat_features),
                ]
            )

            ### MAGIC PART OF PIPELINE!!!
            pipe = Pipeline(
                steps=[
                    ("preprocessor", preprocessor),
                    ("selector", None),
                    ("classifier", model.get("classifier")),
                ]
            )

            print(model.get("name").center(100, "-"))

            brier_multi_loss = make_scorer(
                helper.calculate_brier_multi,
                greater_is_better=False,
                needs_proba=True,
            )

            search = GridSearchCV(
                estimator=pipe,
                param_grid=model.get("param_grid"),
                scoring=brier_multi_loss,
                cv=3,
                n_jobs=-1,
                refit=True,
                verbose=3,
                error_score="raise",
            )
            search.fit(X_train, y_train)

            prediction = search.predict(X_train)

            print()
            print("GridSearchCV:")
            print(f"Best score : {search.best_score_}")
            print(f"Best params: {search.best_params_}")

            print()
            print(f"Score on full data after refit: {search.score(X_train, y_train)}")

            # Precision: Of all the predicted positives, how many were actually positive?
            # Recall: Of all positives, how many did the model said it was positive?
            # F1-score: The harmonic mean of precision and recall.
            print()
            print(classification_report(prediction, y_train, zero_division=0))

            filename = ""
            if self.testrun:
                filename = f"./tests/sources/models/{model.get('name')}.sav"
            else:
                filename = f"./sources/models/{model.get('name')}.sav"
            pickle.dump(search, open(filename, "wb"))

        print(f"Stop: {dt.datetime.now()}")
