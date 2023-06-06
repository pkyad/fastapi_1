FROM python:3.11.3

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY poetry.lock pyproject.toml ./
RUN pip install --upgrade pip && \
    pip install poetry && \
    poetry config virtualenvs.create false 

ARG DEV=true
RUN poetry install

COPY ./app/ ./

ENV PYTHONPATH "${PYTHONPATH}:/app"

EXPOSE 8080
CMD uvicorn main:app --host 0.0.0.0 --port 8080
