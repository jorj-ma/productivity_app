from app import app
from models import db, User, Note
from faker import Faker

fake = Faker()

def seed():
    with app.app_context():
        Note.query.delete()
        User.query.delete()
        db.session.commit()

        users = []
        for _ in range(3):
            user = User(username=fake.unique.user_name())
            user.set_password("password123")
            db.session.add(user)
            users.append(user)
        db.session.commit()

        for user in users:
            for _ in range(5):
                note = Note(
                    title=fake.sentence(nb_words=5).rstrip("."),
                    content=fake.paragraph(nb_sentences=4),
                    user_id=user.id,
                )
                db.session.add(note)
        db.session.commit()
        print(f"Seeded {len(users)} users with 5 notes each.")

if __name__ == "__main__":
    seed()