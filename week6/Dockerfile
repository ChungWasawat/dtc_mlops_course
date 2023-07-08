FROM python:3.10.0-slim

RUN pip install -U pip & pip install pipenv

COPY [ "Pipfile", "Pipfile.lock", "./" ]

RUN pipenv install --system --deploy

COPY [ "hw_batch.py", "hw_batch.py" ]
COPY [ "model.bin", "model.bin" ]

ENTRYPOINT [ "python", "batch.py" ]