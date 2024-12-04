from flask import Flask, jsonify
import pymysql
import os

app = Flask(__name__)

@app.route('/')
def hello():
    # Database connection
    connection = pymysql.connect(
        host=os.getenv('MYSQL_HOST', 'localhost'),
        user=os.getenv('MYSQL_USER', 'root'),
        password=os.getenv('MYSQL_PASSWORD', ''),
        database=os.getenv('MYSQL_DATABASE', '')
    )
    with connection.cursor() as cursor:
        cursor.execute("SHOW DATABASES;")
        databases = cursor.fetchall()
    connection.close()
    return jsonify(databases)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
