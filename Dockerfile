FROM python:3.9-slim

WORKDIR /home/user/stinky-pinky-brain 

# Copy dependency file and install requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your application code
COPY . .

# Set environment variable for the port (adjust if necessary)
ENV PORT 8080
EXPOSE 8080

# Install Gunicorn
RUN pip install gunicorn

# Start the app with Gunicorn
CMD ["gunicorn", "-b", ":8080", "main:app"]
