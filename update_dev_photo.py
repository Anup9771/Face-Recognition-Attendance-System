from app import app, db
from models import Developer

with app.app_context():
    dev = Developer.query.first()
    if dev:
        dev.photo = 'developer.jpeg'
        db.session.commit()
        print("Developer photo updated to developer.jpeg")
    else:
        print("No developer found in database")
