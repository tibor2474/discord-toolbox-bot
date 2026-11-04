# builder
FROM python:3.14-alpine AS build-stage

# set environment
WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH="/app/venv/bin:$PATH"

# set venv and copy requirements
RUN python -m venv /app/venv
COPY requirements.txt .

# install packages
RUN pip install --no-cache-dir -r requirements.txt

# runtime
FROM python:3.14-alpine AS runtime-stage

# set labels
LABEL org.opencontainers.image.authors="tibor2474"
LABEL org.opencontainers.image.title="Toolbox Discord Bot"
LABEL org.opencontainers.image.description="A simple utility Discord bot."
LABEL org.opencontainers.image.documentation="https://github.com/tibor2474/toolbox/blob/main/README.md"
LABEL org.opencontainers.image.source="https://github.com/tibor2474/toolbox"
LABEL org.opencontainers.image.url="https://github.com/tibor2474/toolbox/packages"

# set environment
WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH="/app/venv/bin:$PATH"

# copy files from build-stage
COPY --from=build-stage /app/venv /app/venv
COPY . .

# set volume for logs
VOLUME ["/app/logs"]

# run the app
CMD ["python", "main.py"]