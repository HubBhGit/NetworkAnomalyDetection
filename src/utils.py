import os
import sys
import pickle
from sklearn.metrics import accuracy_score, f1_score
from sklearn.model_selection import GridSearchCV
from src.exception import CustomException

def save_object(file_path, obj):
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)

        with open(file_path, "wb") as file_obj:
            pickle.dump(obj, file_obj)

    except Exception as e:
        raise CustomException(e, sys)

def evaluate_models(X_train, y_train, X_test, y_test, models, param):
    try:
        report = {}

        for i in range(len(list(models))):
            model = list(models.values())[i]
            para = param[list(models.keys())[i]]

            # Hyperparameter tuning with GridSearchCV
            gs = GridSearchCV(model, para, cv=3, scoring='accuracy')
            gs.fit(X_train, y_train)

            # Set the best parameters to the model and retrain it
            model.set_params(**gs.best_params_)
            model.fit(X_train, y_train)

            # Model predictions
            y_train_pred = model.predict(X_train)
            y_test_pred = model.predict(X_test)

            # Evaluate model performance
            train_accuracy = accuracy_score(y_train, y_train_pred)
            test_accuracy = accuracy_score(y_test, y_test_pred)

            train_f1 = f1_score(y_train, y_train_pred, average='weighted')
            test_f1 = f1_score(y_test, y_test_pred, average='weighted')

            # Store test metrics in report dictionary
            report[list(models.keys())[i]] = {
                "Test Accuracy": test_accuracy,
                "Test F1 Score": test_f1,
                "Train Accuracy": train_accuracy,
                "Train F1 Score": train_f1
            }

        return report

    except Exception as e:
        raise CustomException(e, sys)

def load_object(file_path):
    if not file_path:
        raise ValueError("The file path must not be empty.")

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file at {file_path} does not exist.")

    try:
        with open(file_path, "rb") as file_obj:
            return pickle.load(file_obj)
    except (pickle.PickleError, EOFError) as e:
        raise CustomException(f"Error loading object from file: {e}", sys)
    except Exception as e:
        raise CustomException(e, sys)
