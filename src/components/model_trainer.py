import os
import sys
from dataclasses import dataclass 

from catboost import CatBoostClassifier
from sklearn.svm import SVC
from sklearn.ensemble import (
    AdaBoostClassifier,
    GradientBoostingClassifier,
    RandomForestClassifier,
)
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from xgboost import XGBClassifier

from src.exception import CustomException
from sklearn.preprocessing import StandardScaler
from src.logger import logging
from src.utils import save_object, evaluate_models

@dataclass
class ModelTrainerConfig:
    trained_model_file_path = os.path.join("artifacts", "model.pkl")

class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()

    def initiate_model_trainer(self, train_array, test_array):
        try:
            logging.info("Split training and test input data")
            X_train, y_train, X_test, y_test = (
                train_array[:, :-1],
                train_array[:, -1],
                test_array[:, :-1],
                test_array[:, -1]
            )

            # Scale the data
            scaler = StandardScaler()
            X_train = scaler.fit_transform(X_train)
            X_test = scaler.transform(X_test)
            
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

         # params
            params = {
                "Logistic Regression": {
                    'C': [0.01, 0.1, 1, 10],
                    'solver': ['sag', 'saga'],
                    'max_iter': [700, 1000]  # Increased max_iter
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
            
            
            model_report:dict=evaluate_models(X_train=X_train,y_train=y_train,X_test=X_test,y_test=y_test,
                                             models=models,param=params)
            
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

            predicted=best_model.predict(X_test)

            accuracy = accuracy_score(y_test, predicted)
            return accuracy
              
        except Exception as e:
            raise CustomException(e,sys)
        
        
#accuracy = accuracy_score(y_test, predicted) return accuracy