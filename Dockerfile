# Use Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy files
COPY app.py /app

# Install Flask
RUN pip install flask

# Expose port
EXPOSE 5000

# Run the Flask app
CMD ["python", "app.py"]