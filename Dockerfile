FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9
RUN pip install --upgrade pip
WORKDIR /usr/src/fizikservices
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt
COPY api/ /app/api