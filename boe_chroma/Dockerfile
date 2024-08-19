from python:3.10-slim

# Set the working directory

WORKDIR /app

# Copy the current directory contents into the container at /app

COPY . /app

# Create venv

RUN python -m venv venv

# Make venv the active environment

RUN . venv/bin/activate

# Install any needed packages specified in requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

# Make port 80 available to the world outside this container