1. create environment with python 3.9 and install packages in requirements file (pip)
2. start mlflow ui with sqlite as backend to store artifacts
3. on mlflow ui, we can choose specific runs to compare their parameters/ metrics

### ML FLow
    * to choose the best model, aware of duration, size of model

use [MLFLOW autolog](https://mlflow.org/docs/latest/tracking.html#automatic-logging) to log all information about experiment

    * use log_artifact to save preprocessor model (dictVector) and log_model to save model

