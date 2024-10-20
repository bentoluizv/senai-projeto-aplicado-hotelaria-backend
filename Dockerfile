FROM python:3.12.3

RUN apt update; apt upgrade -y

RUN pip install poetry

WORKDIR /app

COPY ./pyproject.toml /app/pyproject.toml

RUN poetry install --without dev

COPY ./app /app/app

EXPOSE 8000

CMD ["poetry", "run", "uvicorn", "--host", "0.0.0.0", "app.app:app"]