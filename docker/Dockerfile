FROM python:3.10.6-slim-buster AS runtime


WORKDIR /app

RUN pip install --upgrade pip
COPY ./requirements.txt .

# Install packages
# --no-cache-dir cache to reduce image size
RUN pip install --no-cache-dir -r requirements.txt

COPY ./src ./src
COPY ./main.py .

ENTRYPOINT python main.py

