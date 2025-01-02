from config import db, ma
from marshmallow_sqlalchemy import fields
from marshmallow import fields as marshmallow_fields

class User(db.Model):
    __tablename__ = "users"
    __table_args__ = {'schema': 'CW2', "extend_existing": True}

    user_id = db.Column("UserID", db.Integer, primary_key=True, autoincrement=True)
    username = db.Column("Username", db.String(100), nullable=False)
    email = db.Column("Email", db.String(100), nullable=False, unique=True)
    password = db.Column("Passwords", db.String(255), nullable=False)
    role = db.Column("Roles", db.String(20), nullable=False)

    trails = db.relationship("Trail", back_populates="user", lazy=True)
    trail_logs = db.relationship("TrailLog", back_populates="user", lazy=True)

class Location(db.Model):
    __tablename__ = "Location"
    __table_args__ = {'schema': 'CW2', "extend_existing": True}

    location_id = db.Column("LocationID", db.Integer, primary_key=True, autoincrement=True)
    city = db.Column("City", db.String(90), nullable=False)
    county = db.Column("County", db.String(60), nullable=True)
    country = db.Column("Country", db.String(30), nullable=False)

    trails = db.relationship("Trail", back_populates="location", lazy=True)

class Type(db.Model):
    __tablename__ = "Type"
    __table_args__ = {'schema': 'CW2', "extend_existing": True}

    type_id = db.Column("TypeID", db.Integer, primary_key=True, autoincrement=True)
    type_name = db.Column("Type", db.String(30), nullable=False)

    trails = db.relationship("Trail", back_populates="type", lazy=True)

class Trail(db.Model):
    __tablename__ = "Trail"
    __table_args__ = {'schema': 'CW2', "extend_existing": True}

    trail_id = db.Column("TrailID", db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column("UserID", db.Integer, db.ForeignKey("CW2.users.UserID"), nullable=False)
    location_id = db.Column("LocationID", db.Integer, db.ForeignKey("CW2.Location.LocationID"), nullable=False)
    type_id = db.Column("TypeID", db.Integer, db.ForeignKey("CW2.Type.TypeID"), nullable=False)
    trail_name = db.Column("TrailName", db.String(90), nullable=False)
    difficulty = db.Column("Difficulty", db.String(20), nullable=False)
    distance = db.Column("Distance", db.Numeric(5, 2), nullable=False)
    elevation = db.Column("Elevation", db.Numeric(5, 2), nullable=False)
    hours = db.Column("Hours", db.Integer, nullable=False)
    minutes = db.Column("Minutes", db.Integer, nullable=False)
    description = db.Column("Description", db.Text, nullable=False)

    user = db.relationship("User", back_populates="trails", lazy=True)
    location = db.relationship("Location", back_populates="trails", lazy=True)
    type = db.relationship("Type", back_populates="trails", lazy=True)
    trail_points = db.relationship("TrailPoint", back_populates="trail", lazy=True)
    trail_logs = db.relationship("TrailLog", back_populates="trail", lazy=True)

class TrailPoint(db.Model):
    __tablename__ = "TrailPoint"
    __table_args__ = {'schema': 'CW2', "extend_existing": True}

    point_id = db.Column("PointID", db.Integer, primary_key=True, autoincrement=True)
    trail_id = db.Column("TrailID", db.Integer, db.ForeignKey("CW2.Trail.TrailID"), nullable=False)
    sequence_order = db.Column("SequenceOrder", db.Integer, nullable=False)
    latitude = db.Column("Latitude", db.Float, nullable=False)
    longitude = db.Column("Longitude", db.Float, nullable=False)

    trail = db.relationship("Trail", back_populates="trail_points", lazy=True)

class TrailLog(db.Model):
    __tablename__ = "TrailLog"
    __table_args__ = {'schema': 'CW2', "extend_existing": True}

    log_id = db.Column("LogID", db.Integer, primary_key=True, autoincrement=True)
    trail_id = db.Column("TrailID", db.Integer, db.ForeignKey("CW2.Trail.TrailID"), nullable=False)
    user_id = db.Column("UserID", db.Integer, db.ForeignKey("CW2.users.UserID"), nullable=False)
    timestamp = db.Column("Timestamp", db.DateTime, nullable=False)

    trail = db.relationship("Trail", back_populates="trail_logs", lazy=True)
    user = db.relationship("User", back_populates="trail_logs", lazy=True)

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        sqla_session = db.session

    trails = marshmallow_fields.Nested("TrailSchema", many=True)

class LocationSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Location
        load_instance = True
        sqla_session = db.session

    trails = marshmallow_fields.Nested("TrailSchema", many=True)

class TypeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Type
        load_instance = True
        sqla_session = db.session

    trails = marshmallow_fields.Nested("TrailSchema", many=True)

class TrailSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Trail
        load_instance = True
        sqla_session = db.session

    trail_points = marshmallow_fields.Nested("TrailPointSchema", many=True)
    trail_logs = marshmallow_fields.Nested("TrailLogSchema", many=True)

class TrailPointSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = TrailPoint
        load_instance = True
        sqla_session = db.session

class TrailLogSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = TrailLog
        load_instance = True
        sqla_session = db.session
