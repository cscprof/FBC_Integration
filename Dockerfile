# 1. Use an official lightweight Python image
FROM python:3.12-slim

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Copy the requirements file first to leverage Docker cache
COPY requirements.txt .

# 4. Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the rest of the application code
COPY . .

# 6. Expose the port Gunicorn will run on
EXPOSE 8000

# 7. Run the application using Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "flasky_server:app"]