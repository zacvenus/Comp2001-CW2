import os

class Config:
    SERVER = os.getenv('DB_SERVER', 'dist-6-505.uopnet.plymouth.ac.uk')
    DATABASE = os.getenv('DB_DATABASE', 'COMP2001_ZVenus')
    USERNAME = os.getenv('DB_USERNAME', 'ZVenus')
    PASSWORD = os.getenv('DB_PASSWORD', 'WefN343*')

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
