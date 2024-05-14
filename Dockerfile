# Use the official Python image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Install Gunicorn and eventlet for WebSocket support
RUN pip install gunicorn eventlet

# Expose the port the app runs on
EXPOSE 5000

# Command to run the app with Gunicorn using eventlet
CMD ["gunicorn", "-k", "eventlet", "-w", "1", "-b", "0.0.0.0:5000", "app:app"]
