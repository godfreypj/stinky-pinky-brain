# Use the official Python 3.11 slim-buster image as the base
FROM python:3.11-slim-buster

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code into the container
COPY . .

# Expose the port your Flask app will run on (default is 5000)
EXPOSE 5000

# Set the command to run your Flask app using Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "main:app"]