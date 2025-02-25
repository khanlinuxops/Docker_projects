from flask import Flask, render_template
import os
import psycopg2

app = Flask(__name__)

# Database Configuration
db_host = os.getenv("DATABASE_HOST", "localhost")
db_user = os.getenv("DATABASE_USER", "postgres")
db_password = os.getenv("DATABASE_PASSWORD", "password")
db_name = os.getenv("DATABASE_NAME", "mydatabase")

# Connect to Database
def get_db_connection():
    return psycopg2.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        dbname=db_name
    )

# Create Table
def create_table():
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100),
            email VARCHAR(100) UNIQUE
        )
        """)
    conn.commit()
    conn.close()

create_table()  # Initialize Database

@app.route('/')
def home():
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
    conn.close()
    return render_template("index.html", users=users)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

