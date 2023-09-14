FROM python:3.9-slim AS build

RUN apt-get update

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY deployments/requirements.txt .
RUN pip install -r requirements.txt

FROM python:3.9-slim

COPY --from=build /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
COPY . /mlops_pipeline
WORKDIR /mlops_pipeline