"""
Script to add Developer/College details to database
Run this file once to add your college details
"""

from app import app, db
from models import Developer

def add_developer_details():
    with app.app_context():
        # Check if developer already exists
        dev = Developer.query.first()
        
        if dev:
            print("Developer details already exist. Updating...")
            # Update existing details
            dev.name = "Your Name"  # Change this
            dev.email = "your.email@college.edu"  # Change this
            dev.contact = "+91-1234567890"  # Change this
            # dev.photo = "your_photo.jpg"  # Optional: Add photo manually to static/images/developer_photos/
        else:
            print("Adding new developer details...")
            # Create new developer entry
            dev = Developer(
                name="Your Name",  # Change this
                email="your.email@college.edu",  # Change this
                contact="+91-1234567890",  # Change this
                photo="default.jpg"  # Optional: Add photo manually
            )
            db.session.add(dev)
        
        db.session.commit()
        print("✅ Developer details added successfully!")
        print(f"Name: {dev.name}")
        print(f"Email: {dev.email}")
        print(f"Contact: {dev.contact}")

if __name__ == "__main__":
    add_developer_details()
