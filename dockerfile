FROM python:3.9
WORKDIR /python_microservice
COPY ./requirements.txt /python_microservice/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /python_microservice/requirements.txt
COPY . /python_microservice
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "80"]