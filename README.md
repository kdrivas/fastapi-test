# test-task

## Contenido
1) Project structure
2) Installation
3) Endpoint
4) Comments

## Project structure

```
spike_challenge
├── README.md
├── api
│   ├── main.py
│   └── requirements.txt
├── data                                # Files for training the RNN model
├── artifacts                           # Store the model and other artifacts
├── model_package                       # Python package for training and preprocessing
│   ├── model
│   │   ├── __init__.py
│   │   ├── __main__.py
│   │   ├── classifier.py
│   │   ├── constants.py
│   │   ├── prediction.py
│   │   ├── training.py
│   │   └── utils.py
│   ├── tests
│   ├── requirements-test.txt
│   ├── requirements.txt
│   └── setup.py
├── infra/chart_api                      # Helm files
│   ├── templates
│   ├── Chart.yaml
│   ├── values.dev.yaml
│   ├── values.prod.yaml
│   └── values.yaml
├── .pre-commit-config.ini
├── pytest.ini
└── Dockerfile
```

## Installation
- If you wanna train the model from scratch, run these commands (This step is not necessary since the artifacts are in the repo):
```
pip install -e model_package 
python -m model training_model artifacts data/names
```
- To run the API, make sure to install local kubernetes cluster. Follow these CLI commands:
```
brew install helm
helm install api-chart . -f values.dev.yaml
```
- Check the deployment succeded:
```
kubectl get deployments
```
- Create a URL for the service, for this example I used minikube:
```
minikube service fastapi-svc-dev
```
- Important! After running the command above, make sure to use the port to sent requests to the api.
<img src="docs/cli_output.png" >

## Endpoint
Note: The port could change depending on the port assigned by minikube
### Health check
Send a request to this route to verify the service is running

**URL** : `localhost:8000/check_service`

**Method** : `GET`

#### Ejemplo

```
curl --location --request GET 'localhost:8000/check_service'
```

#### Respuesta

**Code** : `200 OK`

```json
{
    "Message":"Hello world from service"
}
```

### Prediccion
Consultar por la prediccion de los datos enviados

**URL** : `localhost:8090/get_prediction`

**Method** : `POST`

#### Ejemplo

```
curl --location --request POST 'localhost:62380/get_prediction' \
    --header 'Content-Type: application/json' \
    --data-raw '{"name": "Jordan","n_predictions": 2}' 
```

#### Respuesta

**Code** : `200 OK`

```json
{
    "predictions": ["English","Irish"],
    "probabilities": [-1.2419129610061646,-1.9099189043045044]
}
```

## Comentarios
- Usar una herramienta de monitoreo. Para las predicciones online, de debe implementar una conexion a una BD para el api en donde se guarden las predicciones que el modelo realiza asi como tambien los datos que recibe. Por otro lado, para las predicciones en batch, se guardan las predicciones y los features. Posteriormente, estos datos podran ser contrastados con los datos reales cuando se tengan y ser mostrados por un dashboard u otro medio.
- Respecto a la degradacion del modelo, se puede schedular el entrenamiento cada cierto tiempo de acuerdo a las metricas observadas.

## Mejoras
- Mejorar las pruebas que se han realizado. Por cuestion de tiempo no pude implementar mas.
- Mejorar la infraestructura usando Helm y Kubernetes en lugar de docker-compose