FROM python:3.13.5-slim@sha256:35d6286639af45c8e5707125f91d6b53e59f3821ff01fb2fdef672c95aa1a0fe
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONHASHSEED=0 \
    TZ=UTC \
    LC_ALL=C.UTF-8 \
    LANG=C.UTF-8
WORKDIR /work/alms-core
COPY requirements.txt /work/requirements.txt
RUN pip install --no-cache-dir -r /work/requirements.txt
COPY alms-core/ /work/alms-core/
CMD ["python", "-m", "pytest", "-q", "-W", "error"]
