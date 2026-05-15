# app/models/extensions.py
# This file re-exports the database objects so models can find them easily.
# The actual setup lives in app/extensions.py.

from app.extensions import db, Base

# You can import db and Base from here or directly from app.extensions — both work.