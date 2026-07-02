"""
ARDS Evaluator
"""

import time

from sklearn.metrics import (

    accuracy_score,

    precision_score,

    recall_score,

    f1_score,

    roc_auc_score

)


class Evaluator:

    def evaluate(

        self,

        model,

        X,

        y

    ):

        start = time.time()

        pred = model.predict(X)

        end = time.time()

        result = {

            "Accuracy":

                accuracy_score(

                    y,

                    pred

                ),

            "Precision":

                precision_score(

                    y,

                    pred

                ),

            "Recall":

                recall_score(

                    y,

                    pred

                ),

            "F1":

                f1_score(

                    y,

                    pred

                ),

            "ROC":

                roc_auc_score(

                    y,

                    pred

                ),

            "Inference":

                end-start

        }

        return result