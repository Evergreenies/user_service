import sqlalchemy

from datetime import datetime
from flask import jsonify, redirect, request, url_for
from sqlalchemy.types import UUID
from werkzeug.routing.converters import UUIDConverter

from config import user_app, logger

try:
    from models.users import User, UserSchema
    from models.database_setup import session_maker
except ImportError:
    from app.models.users import User, UserSchema
    from app.models.database_setup import session_maker

user_app.url_map.converters["uuid"] = UUIDConverter


@user_app.route("/users", methods=["POST"])
def user_add():
    try:
        data = request.get_json()
        print(f"DATA ===> {data}")
        with session_maker() as session:
            user = User(
                username=data.get("username"),
                first_name=data.get("first_name"),
                last_name=data.get("last_name"),
                password=data.get("password"),
                email=data.get("email"),
            )
            session.add(user)
            session.commit()
        return "User record inserted successfully", 201
    except sqlalchemy.exc.IntegrityError as e:
        logger.warning("Username or email alredy exists.")
        return "Username or email alredy exists.", 409
    except Exception as e:
        logger.error("while storing user.", exc_info=True)
        return "Somer erroe while storing users record.", 500


@user_app.route("/users", methods=["GET"])
def list_all_users():
    try:
        with session_maker() as session:
            return UserSchema(many=True).dump(session.query(User).all())
    except Exception:
        logger.error("while fetching all users.", exc_info=True)
        return "Some error while fetching users.", 500


@user_app.route("/users/<uuid:user_id>")
def get_user(user_id: UUID):
    try:
        with session_maker() as session:
            _user = session.query(User).get(user_id)
            if not _user:
                return f"User not found with {user_id=}.", 404

            return UserSchema(many=False).dump(_user)
    except sqlalchemy.exc.DataError:
        logger.warning(f"Invalid user_id: {user_id}")
        return f"Invalid {user_id=}", 404
    except Exception:
        logger.error(f"while fetching {user_id=}.", exc_info=True)
        return f"Some error while fetching user: {user_id}.", 500


@user_app.route("/users/<uuid:user_id>", methods=["PUT"])
def update_user(user_id: UUID):
    try:
        with session_maker() as session:
            _user = session.query(User).get(user_id)
            if not _user:
                return f"User not found with {user_id=}", 404
            data = request.get_json()

            if data.get("password") is not None:
                return "Invalid attribute `password`.", 404

            _user_schema = UserSchema(many=False).dump(_user)
            for key in _user_schema.keys():
                if key in ["password", "id", "created_at"]:
                    continue

                value = data.get(key)
                if not value:
                    continue

                setattr(_user, key, value)

            _user.updated_at = datetime.utcnow()

            session.commit()
            session.flush()
        return f"Record {user_id=} updated successfully.", 200
    except sqlalchemy.exc.IntegrityError:
        logger.warning("Username or email alredy exists.")
        return "Username or email alredy exists.", 409
    except Exception:
        logger.error(f"while updating user: {user_id=}", exc_info=True)
        return f"Some error while updating user: {user_id=}", 500


@user_app.route("/users/<uuid:user_id>", methods=["DELETE"])
def delete_user(user_id: UUID):
    try:
        with session_maker() as session:
            _user = session.query(User).get(user_id)
            if not _user:
                return f"User not found with {user_id=}.", 404

            # TODO: need to check relation once borrowing implemented
            session.delete(_user)
            session.commit()
        return f"User {user_id=} deleted successfully.", 200
    except sqlalchemy.exc.DataError:
        logger.warning(f"Invalid user_id: {user_id}")
        return f"Invalid {user_id=}", 404
    except Exception:
        logger.error(f"while deleting user record with {user_id=}", exc_info=True)
        return f"Some error while deleting user: {user_id=}"


@user_app.route("/users/password-reset/<uuid:user_id>", methods=["PUT"])
def update_user_password(user_id: UUID):
    try:
        with session_maker() as session:
            _user = session.query(User).get(user_id)
            if not _user:
                return f"User with {user_id=} does not exist.", 404

            data = request.get_json()
            if data.get("password") is None:
                return "You must pass password inorder to update password."

            _user.password = data.get("password")
            session.commit()
            session.flush()

        return f"Password for user {user_id=} updated successfully.", 200
    except sqlalchemy.exc.DataError:
        logger.warning(f"Invalid user_id: {user_id}")
        return f"Invalid {user_id=}", 404
    except Exception:
        logger.error(f"while updating user password with {user_id=}", exc_info=True)
        return f"Some error while user password with {user_id=}"


@user_app.route("/user/login", methods=["POST"])
def login():
    try:
        with session_maker() as session:
            data = request.get_json()
            username = data.get("username")
            password = data.get("password")

            if not username or not password:
                return "Missins username or password.", 400

            _user = session.query(User).filter_by(username=username).first()
            if not _user:
                return (
                    f"The username {username=} you provided doest not exists in our dataset.",
                    404,
                )

            if not _user.check_password(password):
                return "Invalid password. Please provide correct password.", 401

            _user_schema = UserSchema(many=False).dump(_user)
            return _user_schema, 200
    except Exception:
        logger.error("while logging-in user.", exc_info=True)
        return "Some error while logging-in user."


@user_app.route("/user/logout")
def logout():
    return "User logged out.", 200
