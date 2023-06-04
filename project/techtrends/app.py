import logging
import sqlite3
import sys
from flask import Flask, jsonify, json, render_template, request, url_for, redirect, flash
from werkzeug.exceptions import abort



# Configure the logger
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to get a database connection.
# This function connects to the database with the name `database.db`
def get_db_connection():
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row

    # Increment the connection count
    app.config['DB_CONNECTION_COUNT'] += 1

    return connection

# Function to get a post using its ID
def get_post(post_id):
    connection = get_db_connection()
    post = connection.execute('SELECT * FROM posts WHERE id = ?', (post_id,)).fetchone()
    connection.close()
    return post

# Define the Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'
app.config['DB_CONNECTION_COUNT'] = 0

# Define the main route of the web application
@app.route('/')
def index():
    # Retrieve posts from the database
    connection = get_db_connection()
    posts = connection.execute('SELECT * FROM posts').fetchall()
    connection.close()

    # Log the event
    app.logger.info('Root page accessed')

    return render_template('index.html', posts=posts)

# Define how each individual article is rendered
# If the post ID is not found, a 404 page is shown
@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    if post is None:
        # Log the event
        app.logger.warning('Non-existing article accessed')
        return render_template('404.html'), 404
    else:
        # Log the event
        app.logger.info(f'Article "{post["title"]}" retrieved')
        return render_template('post.html', post=post)

# Define the About Us page
@app.route('/about')
def about():
    # Log the event
    app.logger.info('About Us page accessed')
    return render_template('about.html')

# Define the post creation functionality
@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            connection = get_db_connection()
            connection.execute('INSERT INTO posts (title, content) VALUES (?, ?)', (title, content))
            connection.commit()
            connection.close()

            # Log the event
            app.logger.info(f'New article "{title}" created')

            return redirect(url_for('index'))

    return render_template('create.html')

# Define the metrics endpoint
@app.route('/metrics')
def metrics():
    connection = get_db_connection()
    post_count = connection.execute('SELECT COUNT(*) FROM posts').fetchone()[0]
    connection.close()

    # Log the event
    app.logger.info('Metrics endpoint accessed')

    return jsonify(
        db_connection_count=app.config['DB_CONNECTION_COUNT'],
        post_count=post_count
    )

# Start the application on port 3111
if __name__ == "__main__":
    # Log Python generic logs at DEBUG level to STDOUT
    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setLevel(logging.DEBUG)
    app.logger.addHandler(stdout_handler)

    # Log events to STDERR
    stderr_handler = logging.StreamHandler(sys.stderr)
    stderr_handler.setLevel(logging.WARNING)
    app.logger.addHandler(stderr_handler)

    app.run(host='0.0.0.0', port='3111')
