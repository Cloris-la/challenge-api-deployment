# Use the official Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy the requirements and install
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app
COPY . .

# Set environment variable for Streamlit to run on the correct port (Render provides $PORT)
ENV PORT 8000

# Streamlit needs this to avoid issues in cloud deployment
ENV PYTHONUNBUFFERED=1
ENV STREAMLIT_BROWSER_GATHER_USAGE_STATS=False

# Expose the port
EXPOSE $PORT

# Run the Streamlit app
CMD ["streamlit", "run", "streamlit_app.py", "--server.port=$PORT", "--server.enableCORS=false", "--server.enableXsrfProtection=false", "--server.address=0.0.0.0"]
