import sys, mlflow
from mlflow.models import infer_signature
from sklearn import datasets
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

n_estimators = int(sys.argv[1]) if len(sys.argv) > 1 else 10

X, y = datasets.load_iris(return_X_y=True)
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, random_state=42)
params = {"n_estimators": n_estimators, "random_state": 0}
model = RandomForestClassifier(**params).fit(Xtr, ytr)
acc = accuracy_score(yte, model.predict(Xte))

mlflow.set_tracking_uri("http://127.0.0.1:5000")
mlflow.set_experiment("iris")
with mlflow.start_run():
    mlflow.log_params(params)
    mlflow.log_metric("accuracy", acc)
    mlflow.sklearn.log_model(
        model, name="model",
        skops_trusted_types=["sklearn.tree._tree.Tree"],
        signature=infer_signature(Xtr, model.predict(Xtr)),
        registered_model_name="iris-model")
print("accuracy", acc)
