#!/usr/bin/env python
"""Initialize the database with tables."""

from app import create_app, db

def init_db():
    app = create_app()
    with app.app_context():
        print("Creating database tables...")
        db.create_all()
        print("Database initialized successfully!")

if __name__ == '__main__':
    init_db()
