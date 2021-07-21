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

# copy the content of the local test directory to the working directory
COPY tests/ .

# set PYTHONPATH env variable
ENV PYTHONPATH=/kuro-bot

# commant to run test phase
FROM base as test
CMD ["pytest", "tests/"]

# command to run on container start
CMD [ "python", "src/kuro.py" ]