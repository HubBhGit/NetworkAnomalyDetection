
import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='[%(asctime)]: %(message)s:')


list_of_files=[
".github/workflows/.gitkeep",
f"arifacts/data.csv",
f"arifacts/test.csv",
f"arifacts/train.csv",
f"arifacts/model.pkl",
f"arifacts/preprocessor.pkl",

f"notebook/data/t.csv",

f"src/__init__.py",
f"src/exception.py",
f"src/logger.py",
f"src/utils.py",

f"src/pipeline/__init__.py",
f"src/pipeline/predict_pipeline.py",
f"src/pipeline/train_pipeline.py",

f"src/components/__init__.py",
f"src/components/data_ingestion.py",
f"src/components/data_transformation.py",
f"src/components/model_trainer.py",

    "app.py",
    "setup.py",
    "requirements.txt"
    "research/research.ipynb",
    
]

for filepath in list_of_files:
    filepath=Path(filepath)
    filedir,filename=os.path.split(filepath)
    
    if filedir!="":
        os.makedirs(filedir,exist_ok=True)
        logging.info(f"Creating directory {filedir} for the file : {filename}")
        
    if(not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):
        with open(filepath,"w") as f:
            pass
            logging.info(f"Creating empty file: {filepath}")
            
    else:
        logging.info(f"{filename} is already exists")
        
        
