# test_rtsoft

## REST API - для получения изображений.

Исходный функционал:
- Считывание исходных данных из csv-файла и добавление их в базу данных.
- Валидация данных перед вставкой в базу.
- Получение HTML-страницы с изображением на основании передаваемых параметров запроса.
- Валидация передаваемых значений параметров запроса.
- Документация по API.
- Запуск проекта в docker-контейнерах (FastAPI, postgres, nginx).


## Стек технологий 

<div>
  <a href="https://www.python.org/">
    <img src="https://github.com/devicons/devicon/blob/master/icons/python/python-original-wordmark.svg" title="Python" alt="Python" width="40" height="40"/>&nbsp;
  </a>
  <a href="https://fastapi.tiangolo.com/">
    <img src="https://github.com/devicons/devicon/blob/master/icons/fastapi/fastapi-original.svg" title="Python" alt="Python" width="40" height="40"/>&nbsp;
  </a>
  <a href="https://nginx.org/">
    <img src="https://github.com/devicons/devicon/blob/master/icons/nginx/nginx-original.svg" title="GitHub" alt="GitHub" width="40" height="40"/>&nbsp;
  </a>
  <a href="https://www.postgresql.org/">
    <img src="https://github.com/devicons/devicon/blob/master/icons/postgresql/postgresql-original.svg" title="GitHub" alt="GitHub" width="40" height="40"/>&nbsp;
  </a>
  <a href ="https://www.docker.com/">
    <img src="https://github.com/devicons/devicon/blob/master/icons/docker/docker-original.svg" title="Docker" alt="Docker" width="40" height="40"/>&nbsp;
  </a>
  <a href="https://github.com/">
    <img src="https://github.com/devicons/devicon/blob/master/icons/github/github-original.svg" title="GitHub" alt="GitHub" width="40" height="40"/>&nbsp;
  </a>
</div>

Версии ПО:

- python: 3.10.4;
- fastapi: 0.101.1;
- uvicorn: 0.23.2;
- Docker: 20.10.18;
- docker-compose: 1.26.0;
- pydantic: 2.1.1;
- asyncpg: 0.28;
- Jinja2: 3.1.2.


# Локальный запуск проекта в Docker-контейнерах

Склонировать репозиторий на локальную машину:
```sh
git clone https://github.com/Syzhet/test_rtsoft.git
```

Установите Docker и docker-compose
```sh
sudo apt install docker.io 
sudo curl -L "https://github.com/docker/compose/releases/download/1.26.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

Cоздайте файлы .env, config.env, db.env в директории
infra/ (директория где лежит файл docker-compose.yaml)
(примеры наполнения файлов приведены в файлах example*.env в этой же папке)

Создайте файл data.csv и поместите его в папку core/

В папку static/ поместите файлы изображений с именами соответствующими
указанным в файле data.csv

Параметры запуска описаны в файлах docker-compose.yaml

Перейдите в папку infra/ и запустите docker-compose:
```sh
sudo docker-compose up --build -d
```

После сборки появляется 4 контейнера:

| Контайнер | Описание |
| ------ | ------ |
| rtsoft_app | контейнер с запущенным приложением FastAPI|
| rtsoft_db | контейнер с базой данных postgres|
| rtsoft_nginx | контейнер с запущенным web-сервером nginx|

После развертывания функционал проекта будет доступен по адресам:

http://localhost:8080/api/v1/ - получение HTML-старницы с изображением (параметр запроса ?category[]=название категории);
http://localhost:8080/static/название_изображения.jpg - ссылка на изображение из папки static/ проекта;
http://localhost:8080/docs - ссылка на API документацию Swagger
http://localhost:8080/redoc - ссылка на API документацию Redoc


## Автор проекта

- [Ионов А.В.](https://github.com/Syzhet) - Python разработчик.
