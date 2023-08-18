FROM python:3.10.4-alpine

WORKDIR /rtsoft

COPY requirements.txt .

RUN python -m pip install --upgrade pip &&pip install -r requirements.txt --no-cache-dir

COPY . .

RUN chmod +x ./start.sh

ENTRYPOINT [ "sh", "start.sh" ]