from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class PredictRequest(BaseModel):
    input: str


class PredictResponse(BaseModel):
    output: str


@app.get("/healthz")
def healthz() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/readyz")
def readyz() -> dict[str, str]:
    return {"status": "ready"}


@app.post("/predict")
def predict(request: PredictRequest) -> PredictResponse:
    return PredictResponse(output=request.input)
