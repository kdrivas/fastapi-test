import logging
import pickle
from typing import Dict
from fastapi import FastAPI, status

from model.prediction import predict, load_model


logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(funcName)s - %(message)s",
    level=logging.DEBUG,
)

logger = logging.getLogger(__name__)

# Only load the artifacts the first time
logger.info("Loading artifacts")
model = load_model("/opt/artifacts/model.pt") 
with open("/opt/artifacts/categories.pkl", "rb") as f:
    all_categories = pickle.load(f)

app = FastAPI()


@app.get("/check_service", status_code=status.HTTP_201_CREATED)
def root() -> Dict:
    return {"Message": "Hello world from service"}


@app.post("/get_prediction", status_code=status.HTTP_201_CREATED)
async def get_prediction(payload: Dict) -> Dict:
    """
    Get the prediction for the requested data
    Input:
        data: The data that will be used to predict
    """
    prediction, probs = predict(
        payload["name"],
        payload["n_predictions"],
        model,
        all_categories,
    )

    return {"predictions": prediction, "probabilities": probs}
