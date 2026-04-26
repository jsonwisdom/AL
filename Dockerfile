FROM python:3.11-slim

WORKDIR /app

COPY validators/alms_signature_v0.2/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY validators/alms_signature_v0.2/server_full.py ./server_full.py
COPY merkle ./merkle
COPY anchors ./anchors

ENV PORT=8080

CMD ["python3", "server_full.py"]
