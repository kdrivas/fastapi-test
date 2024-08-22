FROM python:3.10-slim

RUN apt-get update && apt-get install -y build-essential

COPY artifacts/model.pt opt/artifacts/model.pt
COPY artifacts/categories.pkl opt/artifacts/categories.pkl

COPY api/requirements.txt .
RUN pip install -r requirements.txt

COPY model_package model_package
RUN pip install -e model_package/

WORKDIR /app
COPY api .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--port", "8000", "--host", "0.0.0.0"]