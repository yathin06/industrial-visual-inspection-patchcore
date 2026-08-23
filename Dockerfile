FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    libglib2.0-0 \
    libgl1 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN python -m pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY api ./api
COPY src ./src
COPY models ./models

RUN mkdir -p /app/outputs/api_uploads

EXPOSE 8000

CMD ["uvicorn", "api.inspection_api:app", "--host", "0.0.0.0", "--port", "8000"]