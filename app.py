from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_sqlalchemy import SQLAlchemy
import bcrypt
from markupsafe import escape

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "super-secret-key-change-in-production"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///demo.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

jwt = JWTManager(app)
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.LargeBinary, nullable=False)

with app.app_context():
    db.create_all()
    if not User.query.filter_by(username="admin").first():
        hash_pw = bcrypt.hashpw(b"Admin123!", bcrypt.gensalt())
        new_user = User(username="admin", password_hash=hash_pw)
        db.session.add(new_user)
        db.session.commit()


@app.route("/auth/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    user: User = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({"msg": "Bad username or password"}),401
    if bcrypt.checkpw(password.encode("utf-8"), user.password_hash):
        access_token = create_access_token(identity=user.username)
        return jsonify(access_token=access_token),200
    return jsonify({"msg": "Bad username or password"}),401


@app.route("/api/data", methods=["GET"])
@jwt_required()
def get_data():
    users = User.query.all()
    result = []
    for u in users:
        result.append({
            "id": u.id,
            "username": escape(u.username)
        })
    return jsonify(users=result)


@app.route("/api/profile", methods=["GET"])
@jwt_required()
def profile():
    current_user = get_jwt_identity()
    safe_name = escape(current_user)
    return jsonify(logged_in_user=safe_name)

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0")
