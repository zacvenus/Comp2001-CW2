import pathlib
import connexion
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

basedir = pathlib.Path(__file__).parent.resolve()
connex_app = connexion.App(__name__, specification_dir=basedir)

app = connex_app.app
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "mssql+pyodbc:///?odbc_connect="
    "DRIVER={ODBC Driver 18 for SQL Server};"
    "SERVER=dist-6-505.uopnet.plymouth.ac.uk;"
    "DATABASE=COMP2001_ZVenus;"
    "UID=ZVenus;"
    "PWD=WefN343*;"
    "TrustServerCertificate=yes;"
    "Encrypt=yes;"
)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)
