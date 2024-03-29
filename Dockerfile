# set base image (host OS)
FROM python:3.7-slim-buster

# set the working directory in the container
WORKDIR /kuro-bot

# copy the dependencies file to the working directory
COPY requirements.txt .

# install dependencies
RUN pip install -r requirements.txt

# copy the content of the local src directory to the working directory
COPY src/ .

# set PYTHONPATH env variable
ENV PYTHONPATH=/kuro-bot

# Create directory of logs
RUN mkdir -p /kuro-bot/data/logs

# command to run on container start
CMD ["python", "kuro.py"]