from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    user_id    = db.Column(db.Integer, primary_key=True)
    username   = db.Column(db.String(50), unique=True, nullable=False)
    email      = db.Column(db.String(120), unique=True, nullable=False)
    pw_hash    = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    items      = db.relationship('Item', backref='owner', lazy=True)
    locations  = db.relationship('Location', backref='owner', lazy=True)

class Store(db.Model):
    __tablename__ = 'store'
    store_id = db.Column(db.Integer, primary_key=True)
    name     = db.Column(db.String(100), nullable=False)

class Category(db.Model):
    __tablename__ = 'category'
    category_id = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.String(100), nullable=False)

class Location(db.Model):
    __tablename__ = 'location'
    location_id = db.Column(db.Integer, primary_key=True)
    user_id     = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    name        = db.Column(db.String(100), nullable=False)
    parent_id   = db.Column(db.Integer, db.ForeignKey('location.location_id'), nullable=True)
    children    = db.relationship(
        'Location',
        backref=db.backref('parent', remote_side=[location_id]),
        lazy=True
    )

class Item(db.Model):
    __tablename__ = 'item'
    item_id        = db.Column(db.Integer, primary_key=True)
    user_id        = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    store_id       = db.Column(db.Integer, db.ForeignKey('store.store_id'))
    category_id    = db.Column(db.Integer, db.ForeignKey('category.category_id'))
    location_id    = db.Column(db.Integer, db.ForeignKey('location.location_id'))
    name           = db.Column(db.String(100), nullable=False)
    quantity       = db.Column(db.Integer, nullable=False, default=1)
    purchase_price = db.Column(db.Numeric(8,2))
    expires        = db.Column(db.Date)
    purchased_at   = db.Column(db.DateTime, server_default=db.func.now())
    store    = db.relationship('Store',    backref='items')
    category = db.relationship('Category', backref='items')
    location = db.relationship('Location', backref='items')

class ProgramRun(db.Model):
    __tablename__ = 'program_runs'
    id        = db.Column(db.Integer, primary_key=True)
    input     = db.Column(db.String(200))
    output    = db.Column(db.String(200))
    timestamp = db.Column(db.DateTime, server_default=db.func.now())
