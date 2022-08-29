FROM python:3.9-slim

# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED True


# Copy local code to the container image.
COPY . /my_cloud_run
WORKDIR /my_cloud_run

# Install Python Requirements
#RUN pip install -r requirements.txt

# commenting as was getting gunicorn not found error
#RUN pip install poetry
#RUN poetry install

RUN pip install --no-cache-dir -r requirements.txt

# Run the web service on container startup. Here we use the gunicorn
# webserver, with one worker process and 8 threads.
# For environments with multiple CPU cores, increase the number of workers
# to be equal to the cores available.
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 src.main:app