FROM python:3.10.4-alpine

WORKDIR /rtsoft

COPY requirements.txt .

RUN python -m pip install --upgrade pip &&pip install -r requirements.txt --no-cache-dir

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]