from flask import Flask, request, jsonify
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)


# 데이터베이스 연결 설정
def create_db_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            database="your_database_name",
            user="your_mysql_username",
            password="your_mysql_password",
        )
        return connection
    except Error as e:
        print(f"Error connecting to MySQL database: {e}")
        return None


@app.route("/search_accommodation", methods=["POST"])
def search_accommodation():
    location = request.json.get("위치")

    if not location:
        return jsonify({"error": "Location is required"}), 400

    connection = create_db_connection()
    if connection is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM accommodation WHERE address LIKE %s"
        cursor.execute(query, (f"%{location}%",))
        results = cursor.fetchall()

        if not results:
            return (
                jsonify(
                    {"message": f"No accommodation found for the location: {location}"}
                ),
                404,
            )

        return jsonify(results), 200

    except Error as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


if __name__ == "__main__":
    app.run(debug=True)
