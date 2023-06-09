# this file can not be run, it is just an example from the lesson

import xgboost as xgb

from hyperopt import fmin, tpe, hp, STATUS_OK, Trials
from hyperopt.pyll import scope

import pickle

# hyperopt: use bayesian method to find the best hyperparameters
# fmin: optimising hyperparameters by minimising an output
# tpe: tree of parzen estimator(?) algorithm to control the logic/ run the optimisation
# hp: contains different methods to define the search space(?)
# STATUS_OK: status of the output that run successfully
# Trials: keep information of each run
# scope: define a range of interger

train = xgb.DMatrix(X_train, label=y_train)
valid = xgb.DMatrix(X_val, label=y_val)

def objective(params):
    with mlflow.start_run():
        mlflow.set_tag("model", "xgboost")
        mlflow.log_params(params)
        booster = xgb.train(
            params=params,
            dtrain=train,
            num_boost_round=1000,
            # use validation set to control training process (stop when overfitting)
            evals=[(valid, 'validation')],
            # stop when not improving for 50 or more rounds
            early_stopping_rounds=50
        )
        y_pred = booster.predict(valid)
        rmse = mean_squared_error(y_val, y_pred, squared=False)
        mlflow.log_metric("rmse", rmse)

    return {'loss': rmse, 'status': STATUS_OK}

# hyperparameters that we want to track 
search_space = {
    # sampling a range of hyperparameters: loguniform, quniform(return real number so scope.int is needed to convert to integer)
    'max_depth': scope.int(hp.quniform('max_depth', 4, 100, 1)),
    # learning rate range: exp(-3) to exp(0) ~ 0.05 to 1
    'learning_rate': hp.loguniform('learning_rate', -3, 0),
    'reg_alpha': hp.loguniform('reg_alpha', -5, -1),
    'reg_lambda': hp.loguniform('reg_lambda', -6, -1),
    'min_child_weight': hp.loguniform('min_child_weight', -1, 3),
    # regression problem: linear regression
    'objective': 'reg:linear',
    'seed': 42
}

best_result = fmin(
    fn=objective,
    space=search_space,
    algo=tpe.suggest,
    max_evals=50,
    trials=Trials()
)

# record date when the model is transitioned and update other information
from datetime import datetime

date = datetime.today().date()
client.update_model_version(
    name=model_name,
    version=model_version,
    description=f"The model version {model_version} was transitioned to {new_stage} on {date}"
)


# to load the model and test it
def test_model(name, stage, X_test, y_test):
    model = mlflow.pyfunc.load_model(f"models:/{name}/{stage}")
    y_pred = model.predict(X_test)
    return {"rmse": mean_squared_error(y_test, y_pred, squared=False)}

%time test_model(name=model_name, stage="Production", X_test=X_test, y_test=y_test) #%time only works in jupyter notebook?

# transform new data
client.download_artifacts(run_id=run_id, path='preprocessor', dst_path='.')

with open("preprocessor/preprocessor.b", "rb") as f_in:
    dv = pickle.load(f_in)

X_test = preprocess(df, dv)

target = "duration"
y_test = df[target].values