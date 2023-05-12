# Use Python 3.8 base image
FROM python:3.8

# Set working directory to /app
COPY . /app
WORKDIR /app
RUN pip install -r /app/techtrends/requirements.txt

# Expose port 3111
EXPOSE 3111

# Initialize database with pre-defined posts
RUN python /app/techtrends/init_db.py

# Run application at container start
CMD [ "python",  "app.py" ]
