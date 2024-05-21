# Use Python base image
FROM python:3.9

# Set working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install -r requirements.txt

# Copy the Python script and YAML configuration file into the container
COPY python_script.py database_config.yaml ./

# Command to run the Python script
CMD ["python", "python_script.py"]