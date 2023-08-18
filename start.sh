python -m db.initial_db

python -m core.loadcsv

uvicorn app.main:app --host 0.0.0.0 --port 7000