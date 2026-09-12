FROM python:3.12-slim-bookworm

RUN apt-get update && apt-get install --no-install-recommends -y \
        build-essential curl && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

ADD https://astral.sh/uv/install.sh /install.sh
RUN chmod +x /install.sh && /install.sh && rm /install.sh
ENV PATH="/root/.local/bin:${PATH}"

ENV UV_PROJECT_ENVIRONMENT="/opt/venv"

WORKDIR /project

COPY pyproject.toml uv.lock application.properties README.md ./

RUN uv sync

COPY app ./app
COPY main.py ./

ENV PATH="/opt/venv/bin:${PATH}"

EXPOSE 80

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]