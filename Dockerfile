FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9
WORKDIR /usr/src/fizikservices
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt
COPY api/ /app/api