FROM python:3.12.3

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN python -m pip install --upgrade pip \
    && pip install poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-root --only main

COPY . .

EXPOSE 8050

CMD ["uvicorn", "app.app:app", "--host", "0.0.0.0", "--port", "8050"]