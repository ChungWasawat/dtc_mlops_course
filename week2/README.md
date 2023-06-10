1. create environment with python 3.9 and install packages in requirements file (pip)
2. start mlflow ui with sqlite as backend to store artifacts
    ```mlflow ui --backend-store-uri sqlite:///mlflow.db```
    ```mlflow server -h 0.0.0.0 -p 5000 --backend-store-uri postgresql://mlflow:v.....1.rds.amazonaws.com:5432/mlflow_db --default-artifact-root s3://mlflow-artifact-store```
3. on mlflow ui, we can choose specific runs to compare their parameters/ metrics

### ML FLow
    * to choose the best model, aware of duration, size of model

use [MLFLOW autolog](https://mlflow.org/docs/latest/tracking.html#automatic-logging) to log all information about experiment

    * use log_artifact to save preprocessor model (dictVector) and log_model to save model

