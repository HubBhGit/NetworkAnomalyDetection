import os
import sys
from typing import List, Tuple, Generator
from dataclasses import dataclass

from catboost import CatBoostRegressoC
from sklearn.ensemble import (
    AdaBoostClassifier,
    GradientBoostingClassifier,
    RandomForestClassifier,
)
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from sklearn.model_selection import GridSearchCV
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from xgboost import XGBClassifier

from src.exception import CustomException
from src.logger import logging

from src.utils import save_object,evaluate_models

@dataclass
class ModelTrainerConfig:
    trained_model_file_path=os.path.join("artifacts","model.pkl")

class ModelTrainer:
    def __init__(self):
        self.model_trainer_config=ModelTrainerConfig()


    def initiate_model_trainer(self,train_array,test_array):
        try:
            logging.info("Split training and test input data")
            X_train,y_train,X_test,y_test=(
                train_array[:,:-1],
                train_array[:,-1],
                test_array[:,:-1],
                test_array[:,-1]
            )
            models = {
                "LogisticRegression": LogisticRegression(),
                "SVC": SVC(),
                "KNeighborsClassifier": KNeighborsClassifier(),
                "DecisionTreeClassifier": DecisionTreeClassifier(),
                "RandomForestClassifier": RandomForestClassifier(),
                "AdaBoostClassifier": AdaBoostClassifier(),
                "CatBoostClassifier": CatBoostClassifier(),
                "XGBClassifier": XGBClassifier()
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

            model_report:dict=evaluate_models(X_train=X_train,
                                              y_train=y_train,
                                              X_test=X_test,
                                              y_test=y_test,
                                              models=models,
                                              param=params,
                                              metric=accuracy_score
                                              )
            
            ## To get best model score from dict
            best_model_score = max(sorted(model_report.values()))

            ## To get best model name from dict

            best_model_name = list(model_report.keys())[
                list(model_report.values()).index(best_model_score)
            ]
            best_model = models[best_model_name]

            if best_model_score<0.6:
                raise CustomException("No best model found")
            logging.info(f"Best found model on both training and testing dataset")

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
            raise CustomException(e,sys)