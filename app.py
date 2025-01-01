from flask import jsonify, request, abort,redirect
import requests
from datetime import datetime
from config import db, app
from models import Trail, TrailSchema, Location, LocationSchema, Type, TypeSchema, TrailPoint, TrailPointSchema, User, TrailLog
from flasgger import Swagger, swag_from

swagger = Swagger(app)

AUTH_URL = "https://web.socem.plymouth.ac.uk/COMP2001/auth/api/users"

def is_user_admin(user):
    return user.role == 'admin'

def get_user(req):
    email = request.headers.get("x-email")
    user = User.query.filter(User.email == email).one_or_none()
    return user

def is_user_real(req):
    email = req.headers.get("x-email")
    password = req.headers.get("x-password")

    if email is None or password is None:
        return False

    body = {"email": email, "password": password}
    response = requests.post(AUTH_URL, json=body)

    response = response.json()

    return response[1] == 'True'

@app.route("/")
def home():
    return redirect("/apidocs")

@app.route('/trails', methods=['GET'])
@swag_from({
    'responses': {
        200: {
            'description': 'List of all trails',
            'schema': {
                'type': 'array',
                'items': {'$ref': '#/definitions/Trail'}
            }
        },
        500: {
            'description': 'Error fetching trails'
        }
    }
})
def get_trails():
    try:
        trails = Trail.query.all()
        return jsonify(TrailSchema(many=True).dump(trails))
    except Exception as e:
        return jsonify({"error": "Error fetching trails", "details": str(e)}), 500

@app.route('/trails/<int:id>', methods=['GET'])
@swag_from({
    'parameters': [
        {
            'name': 'id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID of the trail'
        }
    ],
    'responses': {
        200: {
            'description': 'Trail details',
            'schema': {'$ref': '#/definitions/Trail'}
        },
        404: {
            'description': 'Trail not found'
        }
    }
})
def get_trail_by_id(id):
    try:
        trail = Trail.query.filter(Trail.trail_id == id).one_or_none()
        if not trail:
            return jsonify({"error": "Trail not found"}), 404

        trail_schema = TrailSchema()
        points = TrailPoint.query.filter(TrailPoint.trail_id == id).all()
        points_schema = TrailPointSchema(many=True)

        trail_data = trail_schema.dump(trail)
        trail_data["points"] = points_schema.dump(points)

        return jsonify(trail_data)
    except Exception as e:
        return jsonify({"error": "Error fetching trail", "details": str(e)}), 500

@app.route('/trails', methods=['POST'])
@swag_from({
    'parameters': [
        {
            'name': 'trail',
            'in': 'body',
            'required': True,
            'schema': {'$ref': '#/definitions/NewTrail'}
        }
    ],
    'responses': {
        201: {
            'description': 'Trail created successfully',
            'schema': {'$ref': '#/definitions/Trail'}
        },
        401: {
            'description': 'Unauthorized credentials'
        }
    }
})
def create_trail():
    if not is_user_real(request):
        abort(401, "Unauthorized credentials")

    user = get_user(request)
    if user is None or not is_user_admin(user):
        abort(401, "Unauthorized credentials")

    try:
        trail_data = request.get_json()
        print("Trail Data:", trail_data) 

        points_data = trail_data.pop("points", [])
        print("Points Data:", points_data) 

        new_trail = Trail(
            user_id=user.user_id,
            trail_name=trail_data['trail_name'],
            difficulty=trail_data['difficulty'],
            distance=trail_data['distance'],
            elevation=trail_data['elevation'],
            hours=trail_data['hours'],
            minutes=trail_data['minutes'],
            description=trail_data['description'],
            location_id=trail_data['location_id'],
            type_id=trail_data['type_id']
        )

        db.session.add(new_trail)
        db.session.commit() 

        trail_id = new_trail.trail_id
        print(f"New Trail ID: {trail_id}")  

        for point in points_data:
            new_point = TrailPoint(
                trail_id=trail_id,  
                sequence_order=point['sequence_order'],
                latitude=point['latitude'],
                longitude=point['longitude']
            )
            db.session.add(new_point)

        db.session.commit()

        new_log = TrailLog(
            trail_id=trail_id,
            user_id=user.user_id,
            timestamp=datetime.now()
        )
        db.session.add(new_log)
        db.session.commit()

        return jsonify({"message": "Trail created successfully", "trail": TrailSchema().dump(new_trail)}), 201

    except Exception as e:
        print("Error details:", str(e))  
        return jsonify({"error": "Error creating trail", "details": str(e)}), 500




@app.route('/trails/<int:id>', methods=['PUT'])
@swag_from({
    'parameters': [
        {
            'name': 'id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID of the trail'
        },
        {
            'name': 'trail',
            'in': 'body',
            'required': True,
            'schema': {'$ref': '#/definitions/NewTrail'}
        }
    ],
    'responses': {
        200: {
            'description': 'Trail updated successfully',
            'schema': {'$ref': '#/definitions/Trail'}
        },
        404: {
            'description': 'Trail not found'
        },
        401: {
            'description': 'Unauthorized credentials'
        }
    }
})
def update_trail(id):
    if not is_user_real(request):
        abort(401, "Unauthorized credentials")

    user = get_user(request)
    if user is None or not is_user_admin(user):
        abort(401, "Unauthorized credentials")

    try:
        trail_data = request.get_json()
        existing_trail = Trail.query.filter(Trail.trail_id == id).one_or_none()

        if existing_trail is None:
            return jsonify({"error": "Trail not found"}), 404

        existing_trail.name = trail_data['name']
        existing_trail.difficulty = trail_data['difficulty']
        existing_trail.distance = trail_data['distance']
        existing_trail.elevation = trail_data['elevation']
        existing_trail.hours = trail_data['hours']
        existing_trail.mins = trail_data['minutes']
        existing_trail.description = trail_data['description']
        existing_trail.location_id = trail_data['location_id']
        existing_trail.type_id = trail_data['type_id']

        db.session.commit()

        for point in trail_data['points']:
            new_point = TrailPoint(
                trail_id=existing_trail.trail_id,
                sequence_order=point['sequence_order'],
                longitude=point['longitude'],
                latitude=point['latitude']
            )
            db.session.add(new_point)

        db.session.commit()

        new_log = TrailLog(
            TrailID=existing_trail.trail_id,
            UserID=user.user_id,
            Timestamp=datetime.now()
        )
        db.session.add(new_log)
        db.session.commit()

        return jsonify({"message": "Trail updated successfully", "trail": TrailSchema().dump(existing_trail)}), 200
    except Exception as e:
        return jsonify({"error": "Error updating trail", "details": str(e)}), 500

@app.route('/trails/<int:id>', methods=['DELETE'])
@swag_from({
    'parameters': [
        {
            'name': 'id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID of the trail to delete'
        }
    ],
    'responses': {
        204: {
            'description': 'Trail deleted successfully'
        },
        404: {
            'description': 'Trail not found'
        },
        401: {
            'description': 'Unauthorized credentials'
        }
    }
})
def delete_trail(id):
    if not is_user_real(request):
        abort(401, "Unauthorized credentials")

    user = get_user(request)
    if user is None or not is_user_admin(user):
        abort(401, "Unauthorized credentials")

    try:
        trail = Trail.query.filter(Trail.trail_id == id).one_or_none()

        if trail is None:
            return jsonify({"error": "Trail not found"}), 404

        for point in trail.trail_points:
            db.session.delete(point)

        db.session.delete(trail)
        db.session.commit()

        return jsonify({"message": "Trail deleted successfully"}), 204
    except Exception as e:
        return jsonify({"error": "Error deleting trail", "details": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
