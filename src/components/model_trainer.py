import os
import sys
from dataclasses import dataclass
from typing import Dict, Any

from catboost import CatBoostClassifier
from sklearn.svm import SVC
from sklearn.ensemble import (
    AdaBoostClassifier,
    GradientBoostingClassifier,
    RandomForestClassifier,
)
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from xgboost import XGBClassifier

from src.exception import CustomException
from src.logger import logging
from src.utils import save_object, evaluate_models

@dataclass
class ModelTrainerConfig:
    trained_model_file_path = os.path.join("artifacts", "model.pkl")

class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()

    def initiate_model_trainer(self, train_array: Any, test_array: Any) -> Dict[str, Any]:
        try:
            logging.info("Splitting training and test input data")
            X_train, y_train, X_test, y_test = (
                train_array[:, :-1],
                train_array[:, -1],
                test_array[:, :-1],
                test_array[:, -1]
            )

            models = {
                "Logistic Regression": LogisticRegression(),
                "Support Vector Classifier": SVC(),
                "K-Neighbors Classifier": KNeighborsClassifier(),
                "Decision Tree Classifier": DecisionTreeClassifier(),
                "Random Forest Classifier": RandomForestClassifier(),
                "AdaBoost Classifier": AdaBoostClassifier(),
                "Gradient Boosting Classifier": GradientBoostingClassifier(),
                "CatBoost Classifier": CatBoostClassifier(verbose=False),
                "XGBoost Classifier": XGBClassifier()
            }

            params = {
                "Logistic Regression": {
                    'C': [0.01, 0.1, 1, 10],
                    'solver': ['liblinear', 'lbfgs']
                },
                "Support Vector Classifier": {
                    'C': [0.1, 1, 10],
                    'kernel': ['linear', 'rbf', 'poly']
                },
                "K-Neighbors Classifier": {
                    'n_neighbors': [3, 5, 7, 9]
                },
                "Decision Tree Classifier": {
                    'criterion': ['gini', 'entropy'],
                    'max_depth': [5, 10, 15]
                },
                "Random Forest Classifier": {
                    'n_estimators': [50, 100, 150],
                    'criterion': ['gini', 'entropy']
                },
                "AdaBoost Classifier": {
                    'n_estimators': [50, 100],
                    'learning_rate': [0.01, 0.1, 1]
                },
                "Gradient Boosting Classifier": {
                    'n_estimators': [50, 100, 150],
                    'learning_rate': [0.01, 0.1, 0.2]
                },
                "CatBoost Classifier": {
                    'depth': [6, 8, 10],
                    'learning_rate': [0.01, 0.05, 0.1],
                    'iterations': [30, 50, 100]
                },
                "XGBoost Classifier": {
                    'learning_rate': [0.01, 0.05, 0.1],
                    'n_estimators': [50, 100, 150]
                }
            }

            logging.info("Evaluating models with provided parameters")
            model_report = evaluate_models(
                X_train=X_train,
                y_train=y_train,
                X_test=X_test,
                y_test=y_test,
                models=models,
                param=params,
                metric=accuracy_score
            )

            best_model_score = max(model_report.values())
            best_model_name = max(model_report, key=model_report.get)
            best_model = models[best_model_name]

            if best_model_score < 0.6:
                raise CustomException("No suitable model found with acceptable accuracy")

            logging.info(f"Best model found: {best_model_name} with accuracy score: {best_model_score}")

            save_object(
                file_path=self.model_trainer_config.trained_model_file_path,
                obj=best_model
            )

            predicted = best_model.predict(X_test)
            accuracy = accuracy_score(y_test, predicted)
            f1 = f1_score(y_test, predicted, average='weighted')

            return {
                "accuracy_score": accuracy,
                "f1_score": f1,
                "best_model_name": best_model_name
            }

        except Exception as e:
            raise CustomException(e, sys)
