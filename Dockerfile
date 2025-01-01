FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH="/opt/venv/bin:$PATH"
ENV DATABASE_SERVER="dist-6-505.uopnet.plymouth.ac.uk"

RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    libssl-dev \
    libffi-dev \
    libpq-dev \
    unixodbc \
    unixodbc-dev \
    && curl https://sh.rustup.rs -sSf | bash -s -- -y \
    && export PATH="$HOME/.cargo/bin:$PATH" \
    && rm -rf /var/lib/apt/lists/*

RUN python -m venv /opt/venv
RUN python -m pip install --no-cache-dir --upgrade pip setuptools

COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt && rm /tmp/requirements.txt

WORKDIR /app
COPY . /app

RUN adduser --disabled-password --gecos "" --uid 5678 appuser && chown -R appuser /app
USER appuser

CMD ["python", "app.py"]
