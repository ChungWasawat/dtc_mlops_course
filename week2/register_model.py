import os
import pickle
import click
import mlflow

from mlflow.entities import ViewType
from mlflow.tracking import MlflowClient
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error

HPO_EXPERIMENT_NAME = "random-forest-hyperopt"
EXPERIMENT_NAME = "random-forest-best-models"
RF_PARAMS = ['max_depth', 'n_estimators', 'min_samples_split', 'min_samples_leaf', 'random_state', 'n_jobs']

mlflow.set_tracking_uri("http://127.0.0.1:5000")
mlflow.set_experiment(EXPERIMENT_NAME)
mlflow.sklearn.autolog()

mlflow.set_tag("rmse", "test_dataset")


def load_pickle(filename):
    with open(filename, "rb") as f_in:
        return pickle.load(f_in)


def train_and_log_model(data_path, params):
    X_train, y_train = load_pickle(os.path.join(data_path, "train.pkl"))
    X_val, y_val = load_pickle(os.path.join(data_path, "val.pkl"))
    X_test, y_test = load_pickle(os.path.join(data_path, "test.pkl"))

    with mlflow.start_run():
        for param in RF_PARAMS:
            params[param] = int(params[param])

        rf = RandomForestRegressor(**params)
        rf.fit(X_train, y_train)

        # Evaluate model on the validation and test sets
        val_rmse = mean_squared_error(y_val, rf.predict(X_val), squared=False)
        mlflow.log_metric("val_rmse", val_rmse)
        test_rmse = mean_squared_error(y_test, rf.predict(X_test), squared=False)
        mlflow.log_metric("test_rmse", test_rmse)


@click.command()
@click.option(
    "--data_path",
    default="./output",
    help="Location where the processed NYC taxi trip data was saved"
)
@click.option(
    "--top_n",
    default=5,
    type=int,
    help="Number of top models that need to be evaluated to decide which one to promote"
)
def run_register_model(data_path: str, top_n: int):

    # can set tracking uri here
    client = MlflowClient()

    # Retrieve the top_n model runs and log the models
    # client.list_experiments() to see all experiments
    # client.create_experiment(name"NAME") to create a new experiment
    experiment = client.get_experiment_by_name(HPO_EXPERIMENT_NAME)
    runs = client.search_runs(
        experiment_ids=experiment.experiment_id,
        # filter_string="metrics.rmse < 6.8",
        run_view_type=ViewType.ACTIVE_ONLY, 
        # how many runs to return
        max_results=top_n,
        order_by=["metrics.rmse ASC"]
    )
    for run in runs:
        # run.info.run_id is the id of the run
        # run.data.metrics["rmse"] 
        train_and_log_model(data_path=data_path, params=run.data.params)

    # Select the model with the lowest test RMSE
    experiment = client.get_experiment_by_name(EXPERIMENT_NAME)
    best_run = client.search_runs( 
        experiment_ids=experiment.experiment_id,
        run_view_type=ViewType.ACTIVE_ONLY,
        max_results=top_n,
        order_by=["metrics.test_rmse ASC"]       
    )[0]

    best_model_uri = f"runs:/{best_run.info.run_id}/model"
    # Register the best model
    mlflow.register_model( 
        model_uri=best_model_uri,
        name="nyc-taxi-random-forest-model",
    )
    # client.list_registered_models() to see all registered models
    # latest_ver = client.get_latest_versions(name="MODEL_NAME", stages=["Staging"])
    # ver = laest_ver[0] -> ver.current_stage 
    # client.transition_model_version_stage(name="MODEL_NAME", version=ver.version, stage="Production", archive_existing_versions=True)


if __name__ == '__main__':
    run_register_model()