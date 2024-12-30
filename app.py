import pyodbc

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
    f"TrustServerCertificate=yes;"
)

try:
    conn = pyodbc.connect(connectionString)
    cursor = conn.cursor()

    SQL_QUERY = "SELECT * FROM CW2.TrailDetails;"
    cursor.execute(SQL_QUERY)

    for row in cursor.fetchall():
        print(row)

except pyodbc.Error as e:
    print("Database connection failed:", e)

finally:
    if 'conn' in locals() and conn:
        conn.close()
