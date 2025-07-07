# Use official Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy all files into container
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port dynamically provided by Render
ENV PORT=8000

# Start the app using uvicorn on the correct port
CMD ["sh", "-c", "uvicorn app:app --host 0.0.0.0 --port $PORT"]
