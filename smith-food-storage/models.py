from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class FoodItem(db.Model):
    id       = db.Column(db.Integer, primary_key=True)
    name     = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    expires  = db.Column(db.Date, nullable=False)
    location = db.Column(db.String(100))
    timestamp= db.Column(db.DateTime, server_default=db.func.now())

# Optional: store your program runs
class ProgramRun(db.Model):
    id        = db.Column(db.Integer, primary_key=True)
    input     = db.Column(db.String(200))
    output    = db.Column(db.String(200))
    timestamp = db.Column(db.DateTime, server_default=db.func.now())
