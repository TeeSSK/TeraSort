FROM python:3.10.2-bullseye

WORKDIR /app/
COPY dockerfile /app/
COPY gigaSort.py /app/

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir --upgrade numpy

ENTRYPOINT [ "python", "./gigaSort.py" ]