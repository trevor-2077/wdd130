from flask import Flask, render_template, request, redirect, url_for
from config import Config
from models import db, User, Store, Category, Location, Item, ProgramRun
from student_program.core import (
    get_expiring_items,
    total_inventory_value,
    count_by_location,
    format_report
)

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

# -- Startup: create tables & seed defaults --
with app.app_context():
    # 1) Create all tables
    db.create_all()

    # 2) Seed a default user so user_id=1 exists
    if not User.query.first():
        default_user = User(
            username='trevor',
            email='trevor@example.com',
            pw_hash='password-placeholder'
        )
        db.session.add(default_user)

    # 3) Seed Store
    if not Store.query.first():
        db.session.add_all([
            Store(name='Walmart'),
            Store(name="Sam's Club"),
        ])

    # 4) Seed Category
    if not Category.query.first():
        db.session.add_all([
            Category(name='Cereal'),
            Category(name='Drinks'),
            Category(name='Cans'),
        ])

    # 5) Seed Location for user_id=1
    if not Location.query.filter_by(user_id=1).first():
        db.session.add_all([
            Location(user_id=1, name='Pantry'),
            Location(user_id=1, name='Storage Room'),
            Location(user_id=1, name='Cabinet'),
        ])

    db.session.commit()

# -- Routes --

@app.route('/')
def home():
    return redirect(url_for('add_food'))

@app.route('/add', methods=['GET', 'POST'])
def add_food():
    if request.method == 'POST':
        item = Item(
            user_id        = 1,
            name           = request.form['name'],
            quantity       = int(request.form['quantity']),
            expires        = request.form.get('expires') or None,
            purchase_price = request.form.get('purchase_price') or None,
            store_id       = request.form.get('store_id') or None,
            category_id    = request.form.get('category_id') or None,
            location_id    = request.form.get('location_id') or None
        )
        db.session.add(item)
        db.session.commit()
        return redirect(url_for('storage'))

    stores     = Store.query.all()
    categories = Category.query.all()
    locations  = Location.query.filter_by(user_id=1).all()
    return render_template(
        'add.html',
        stores=stores,
        categories=categories,
        locations=locations
    )

@app.route('/storage')
def storage():
    items = Item.query.filter_by(user_id=1).order_by(Item.expires).all()
    return render_template('storage.html', items=items)

@app.route('/program', methods=['GET', 'POST'])
def run_program():
    result = None
    if request.method == 'POST':
        days = int(request.form['x'])
        data = get_expiring_items(days)
        result = format_report(data)

        # Log each run
        run = ProgramRun(input=str(days), output=result)
        db.session.add(run)
        db.session.commit()

    return render_template('program.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
