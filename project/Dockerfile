# Use Python 3.11 base image
FROM python:3.9

# Set working directory to /app
COPY . /app
WORKDIR /app
RUN pip3 install -r requirements.txt

# Expose port 3111
EXPOSE 3111

# Initialize database with pre-defined posts
RUN python3 init_db.py

# Run application at container start
CMD [ "python3",  "app.py" ]
