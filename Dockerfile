FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt requirements-dev.txt ./
RUN python -m pip install --no-cache-dir -r requirements-dev.txt

COPY src ./src
COPY scripts ./scripts
COPY tests ./tests
COPY migrations ./migrations
COPY alembic.ini pyproject.toml ./

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
