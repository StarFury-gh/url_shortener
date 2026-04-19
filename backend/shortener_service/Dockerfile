FROM python:3.12-slim AS build

ENV VIRTUAL_ENV="/opt/venv"
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH "$VIRTUAL_ENV/bin:$PATH"

COPY requirements.txt .
RUN pip install --no-cache-dir -Ur requirements.txt


FROM python:3.12-slim AS runner

COPY --from=build /opt/venv /opt/venv
ENV PATH "/opt/venv/bin:$PATH"

WORKDIR /app
COPY src src
COPY .env .env
CMD ["python3", "src/main.py"]