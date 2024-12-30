from flask import Flask, jsonify, request, render_template
import pyodbc
import config

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/trails', methods=['GET'])
def get_trails():
    try:
        conn = pyodbc.connect(config.connectionString)
        cursor = conn.cursor()
        SQL_QUERY = "SELECT * FROM CW2.TrailDetails;"
        cursor.execute(SQL_QUERY)
        trails = []
        for row in cursor.fetchall():
            trail = {
                'TrailID': row[0],
                'TrailName': row[1],
                'Difficulty': row[2],
                'UserName': row[3],
                'City': row[4],
                'County': row[5],
                'Country': row[6],
                'Distance': row[7],
                'Elevation': row[8],
                'Hours': row[9],
                'Minutes': row[10],
                'Type': row[11],
                'Description': row[12]
            }
            trails.append(trail)
        return jsonify(trails)
    except pyodbc.Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if 'conn' in locals() and conn:
            conn.close()

@app.route('/trails', methods=['POST'])
def add_trail():
    new_trail = request.get_json()
    try:
        conn = pyodbc.connect(config.connectionString)
        cursor = conn.cursor()
        SQL_QUERY = """
            INSERT INTO CW2.TrailDetails (TrailName, Difficulty, UserName, City, County, Country, Distance, Elevation, Hours, Minutes, Type, Description)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        cursor.execute(SQL_QUERY, (
            new_trail['TrailName'], new_trail['Difficulty'], new_trail['UserName'],
            new_trail['City'], new_trail['County'], new_trail['Country'],
            new_trail['Distance'], new_trail['Elevation'], new_trail['Hours'],
            new_trail['Minutes'], new_trail['Type'], new_trail['Description']
        ))
        conn.commit()
        return jsonify(new_trail), 201
    except pyodbc.Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if 'conn' in locals() and conn:
            conn.close()

@app.route('/trails/<int:id>', methods=['DELETE'])
def delete_trail(id):
    try:
        conn = pyodbc.connect(config.connectionString)
        cursor = conn.cursor()
        SQL_QUERY = "DELETE FROM CW2.TrailDetails WHERE TrailID = ?"
        cursor.execute(SQL_QUERY, (id,))
        conn.commit()
        return '', 204
    except pyodbc.Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if 'conn' in locals() and conn:
            conn.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
