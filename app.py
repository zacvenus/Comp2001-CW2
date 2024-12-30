from flask import Flask, request, jsonify
import pyodbc

app = Flask(__name__)

# Database connection
SERVER = 'dist-6-505.uopnet.plymouth.ac.uk'
DATABASE = 'COMP2001_ZVenus'
USERNAME = 'ZVenus'
PASSWORD = 'WefN343*'

connectionString = (
    f"DRIVER={{ODBC Driver 18 for SQL Server}};"
    f"SERVER={SERVER};"
    f"DATABASE={DATABASE};"
    f"UID={USERNAME};"
    f"PWD={PASSWORD};"
    "TrustServerCertificate=yes;"
    "Encrypt"
    "Trusted_Connection=No"
)

# Helper function for DB connection
def get_db_connection():
    try:
        conn = pyodbc.connect(connectionString)
        return conn
    except pyodbc.Error as e:
        print("Database connection failed:", e)
        return None

# Routes
@app.route('/trails', methods=['GET'])
def get_trails():
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM CW2.TrailDetails;")
        trails = [dict(zip([column[0] for column in cursor.description], row)) for row in cursor.fetchall()]
        return jsonify(trails), 200
    finally:
        conn.close()

@app.route('/trails', methods=['POST'])
def add_trail():
    data = request.json
    required_fields = ['TrailName', 'UserName', 'Distance', 'Country']
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO CW2.TrailDetails (TrailName, Difficulty, UserName, City, County, Country, Distance, Elevation, Hours, Minutes, Type, Description) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);",
            data.get('TrailName'), data.get('Difficulty'), data.get('UserName'), data.get('City'), data.get('County'),
            data.get('Country'), data.get('Distance'), data.get('Elevation'), data.get('Hours'), data.get('Minutes'),
            data.get('Type'), data.get('Description')
        )
        conn.commit()
        return jsonify({"message": "Trail added successfully"}), 201
    finally:
        conn.close()

@app.route('/trails/<int:id>', methods=['GET'])
def get_trail_by_id(id):
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM CW2.TrailDetails WHERE TrailID = ?;", id)
        row = cursor.fetchone()
        if not row:
            return jsonify({"error": "Trail not found"}), 404
        trail = dict(zip([column[0] for column in cursor.description], row))
        return jsonify(trail), 200
    finally:
        conn.close()

@app.route('/trails/<int:id>', methods=['PUT'])
def update_trail(id):
    data = request.json
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    try:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE CW2.TrailDetails SET TrailName = ?, Difficulty = ?, UserName = ?, City = ?, County = ?, Country = ?, Distance = ?, Elevation = ?, Hours = ?, Minutes = ?, Type = ?, Description = ? WHERE TrailID = ?;",
            data.get('TrailName'), data.get('Difficulty'), data.get('UserName'), data.get('City'), data.get('County'),
            data.get('Country'), data.get('Distance'), data.get('Elevation'), data.get('Hours'), data.get('Minutes'),
            data.get('Type'), data.get('Description'), id
        )
        if cursor.rowcount == 0:
            return jsonify({"error": "Trail not found"}), 404
        conn.commit()
        return jsonify({"message": "Trail updated successfully"}), 200
    finally:
        conn.close()

@app.route('/trails/<int:id>', methods=['DELETE'])
def delete_trail(id):
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM CW2.TrailDetails WHERE TrailID = ?;", id)
        if cursor.rowcount == 0:
            return jsonify({"error": "Trail not found"}), 404
        conn.commit()
        return '', 204
    finally:
        conn.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
