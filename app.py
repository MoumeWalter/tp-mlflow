import os, random
import numpy as np
from contextlib import asynccontextmanager
import mlflow
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

URI = os.getenv("MLFLOW_TRACKING_URI", "http://127.0.0.1:5000")
NAME = os.getenv("MODEL_NAME", "iris-model")
P_CURRENT = float(os.getenv("P_CURRENT", "0.8"))
mlflow.set_tracking_uri(URI)
state = {}

def load(version):
    return mlflow.pyfunc.load_model(f"models:/{NAME}/{version}")

def latest():
    vs = mlflow.MlflowClient().search_model_versions(f"name='{NAME}'")
    return str(max(int(v.version) for v in vs))

@asynccontextmanager
async def lifespan(app):
    v = latest()
    state.update(current=load(v), next=load(v), cur_v=v, next_v=v)
    yield

app = FastAPI(lifespan=lifespan)

class Req(BaseModel):
    features: list[list[float]]

class Upd(BaseModel):
    version: str

@app.get("/status")
def status():
    return {"current_version": state["cur_v"], "next_version": state["next_v"],
            "p_current": P_CURRENT}

@app.post("/predict")
def predict(r: Req):
    use_current = random.random() < P_CURRENT
    key = "current" if use_current else "next"
    pred = state[key].predict(np.array(r.features, dtype=np.float64))
    return {"prediction": [int(p) for p in pred], "used": key,
            "version": state["cur_v" if use_current else "next_v"]}

@app.post("/update-model")
def update(u: Upd):
    try:
        state["next"], state["next_v"] = load(u.version), u.version
    except Exception as e:
        raise HTTPException(404, str(e))
    return {"next_version": u.version}

@app.post("/accept-next-model")
def accept():
    state["current"], state["cur_v"] = state["next"], state["next_v"]
    return {"current_version": state["cur_v"]}
