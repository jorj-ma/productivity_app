from flask import request, session
from flask_restful import Resource
from config import app, api, db
from models import User, Note

def get_current_user():
    user_id = session.get("user_id")
    if not user_id:
        return None
    return User.query.get(user_id)

class Signup(Resource):
    def post(self):
        data = request.get_json()
        username = data.get("username", "").strip()
        password = data.get("password", "")

        if not username or not password:
            return {"error": "Username and password are required."}, 422
        if User.query.filter_by(username=username).first():
            return {"error": "Username already taken."}, 422

        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        session["user_id"] = user.id
        return user.to_dict(), 201

class Login(Resource):
    def post(self):
        data = request.get_json()
        username = data.get("username", "").strip()
        password = data.get("password", "")

        user = User.query.filter_by(username=username).first()
        if not user or not user.check_password(password):
            return {"error": "Invalid username or password."}, 401
        session["user_id"] = user.id
        return user.to_dict(), 200

class Logout(Resource):
    def delete(self):
        if not get_current_user():
            return {"error": "Not logged in."}, 401
        session.pop("user_id", None)
        return {}, 204

class Me(Resource):
    def get(self):
        user = get_current_user()
        if not user:
            return {"error": "Unauthorized."}, 401
        return user.to_dict(), 200

class NoteList(Resource):
    def get(self):
        user = get_current_user()
        if not user:
            return {"error": "Unauthorized."}, 401
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 10, type=int)

        pagination = (
            Note.query.filter_by(user_id=user.id)
            .order_by(Note.created_at.desc())
            .paginate(page=page, per_page=per_page, error_out=False)
        )
        return {
            "notes": [n.to_dict() for n in pagination.items],
            "total": pagination.total,
            "pages": pagination.pages,
            "page": pagination.page,
        }, 200

    def post(self):
        user = get_current_user()
        if not user:
            return {"error": "Unauthorized."}, 401
        data = request.get_json()
        title = data.get("title", "").strip()
        content = data.get("content", "").strip()

        if not title or not content:
            return {"error": "Title and content are required."}, 422
        note = Note(title=title, content=content, user_id=user.id)
        db.session.add(note)
        db.session.commit()
        return note.to_dict(), 201

class NoteDetail(Resource):
    def _get_owned_note(self, note_id):
        user = get_current_user()
        if not user:
            return None, ({"error": "Unauthorized."}, 401)
        note = Note.query.get(note_id)
        if not note:
            return None, ({"error": "Note not found."}, 404)
        if note.user_id != user.id:
            return None, ({"error": "Forbidden."}, 403)

        return note, None

    def patch(self, note_id):
        note, err = self._get_owned_note(note_id)
        if err:
            return err

        data = request.get_json()
        if "title" in data:
            note.title = data["title"].strip()
        if "content" in data:
            note.content = data["content"].strip()

        db.session.commit()
        return note.to_dict(), 200

    def delete(self, note_id):
        note, err = self._get_owned_note(note_id)
        if err:
            return err

        db.session.delete(note)
        db.session.commit()
        return {}, 204

api.add_resource(Signup,     "/signup")
api.add_resource(Login,      "/login")
api.add_resource(Logout,     "/logout")
api.add_resource(Me,         "/me", "/check_session")
api.add_resource(NoteList,   "/notes")
api.add_resource(NoteDetail, "/notes/<int:note_id>")

if __name__ == "__main__":
    app.run(debug=True)