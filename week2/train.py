import os
import pickle
import click
import mlflow

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error


def load_pickle(filename: str):
    with open(filename, "rb") as f_in:
        return pickle.load(f_in)


@click.command()
@click.option(
    "--data_path",
    default="./output",
    help="Location where the processed NYC taxi trip data was saved"
)
def run_train(data_path: str):

    X_train, y_train = load_pickle(os.path.join(data_path, "train.pkl"))
    X_val, y_val = load_pickle(os.path.join(data_path, "val.pkl"))

    mlflow.autolog()
    with mlflow.start_run():
        # mlflow.set_tag("dev", "wasawat")

        rf = RandomForestRegressor(max_depth=10, random_state=0)
        # tag each parameter (1 by 1) or pass parameters as a dictionary
        # mlflow.log_param("max_depth", max_depth)

        rf.fit(X_train, y_train)
        y_pred = rf.predict(X_val)

        rmse = mean_squared_error(y_val, y_pred, squared=False)
        # tag each metric
        # mlflow.log_metric("rmse", rmse)
        
        # store model 
        # local path: where the model is, artifact path: where the model is stored in mlflow
        # results = only the binary file
        # mlflow.log_artifact(local_path="models/lin_reg.bin", artifact_path="models_pickle")
        # or use model instead of local path
        # results = model + conda.yaml (a version of packages) + MLmodel + requirements.txt
        # mlflow.xgboost.log_model(booster, artifact_path="models_mlflow")



if __name__ == '__main__':
    mlflow.set_tracking_uri("sqlite:///mlflow.db")
    mlflow.set_experiment("homework_week2")
    run_train()