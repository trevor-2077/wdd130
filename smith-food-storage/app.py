from flask import Flask, render_template, request, redirect, url_for, jsonify, abort
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
    db.create_all()

    if not User.query.first():
        db.session.add(
            User(username='trevor', email='trevor@example.com', pw_hash='password-placeholder')
        )

    if not Store.query.first():
        db.session.add_all([
            Store(name='Walmart'),
            Store(name="Sam's Club"),
        ])

    if not Category.query.first():
        db.session.add_all([
            Category(name='Cereal'),
            Category(name='Drinks'),
            Category(name='Cans'),
        ])

    if not Location.query.filter_by(user_id=1).first():
        db.session.add_all([
            Location(user_id=1, name='Pantry'),
            Location(user_id=1, name='Storage Room'),
            Location(user_id=1, name='Cabinet'),
        ])

    db.session.commit()


# -- Routes ----------------------------------------------------

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/add', methods=['GET', 'POST'])
def add_food():
    stores     = Store.query.all()
    categories = Category.query.all()
    locations  = Location.query.filter_by(user_id=1).all()

    if request.method == 'POST':
        names           = request.form.getlist('name[]')
        quantities      = request.form.getlist('quantity[]')
        expirations     = request.form.getlist('expires[]')
        prices          = request.form.getlist('purchase_price[]')
        store_ids       = request.form.getlist('store_id[]')
        new_stores      = request.form.getlist('new_store[]')
        category_ids    = request.form.getlist('category_id[]')
        new_categories  = request.form.getlist('new_category[]')
        location_ids    = request.form.getlist('location_id[]')
        new_locations   = request.form.getlist('new_location[]')

        for i, name in enumerate(names):
            # 1) determine or create Store
            sid = store_ids[i]
            if new_stores[i].strip():
                s = Store(name=new_stores[i].strip())
                db.session.add(s)
                db.session.flush()
                sid = s.store_id
            sid = int(sid) if sid else None

            # 2) determine or create Category
            cid = category_ids[i]
            if new_categories[i].strip():
                c = Category(name=new_categories[i].strip())
                db.session.add(c)
                db.session.flush()
                cid = c.category_id
            cid = int(cid) if cid else None

            # 3) determine or create Location
            lid = location_ids[i]
            if new_locations[i].strip():
                l = Location(user_id=1, name=new_locations[i].strip(), parent_id=None)
                db.session.add(l)
                db.session.flush()
                lid = l.location_id
            lid = int(lid) if lid else None

            # 4) create the Item
            item = Item(
                user_id        = 1,
                name           = name.strip(),
                quantity       = int(quantities[i] or 0),
                expires        = expirations[i] or None,
                purchase_price = prices[i] or None,
                store_id       = sid,
                category_id    = cid,
                location_id    = lid,
            )
            db.session.add(item)

        db.session.commit()
        return redirect(url_for('storage'))

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


@app.route('/delete/<int:item_id>', methods=['POST'])
def delete_item(item_id):
    item = Item.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for('storage'))


@app.route('/edit-item/<int:item_id>', methods=['POST'])
def edit_item(item_id):
    item = Item.query.get_or_404(item_id)
    field = request.form.get('field')
    value = request.form.get('value') or None

    # allow name, quantity, expires, and now location
    if field not in {'name', 'quantity', 'expires', 'location'}:
        return jsonify(error='Invalid field'), 400

    if field == 'quantity':
        try:
            item.quantity = int(value)
        except ValueError:
            return jsonify(error='Quantity must be a number'), 400

    elif field == 'expires':
        item.expires = value

    elif field == 'location':
        # rename shared Location or create a new one
        if item.location:
            item.location.name = value
        else:
            new_loc = Location(user_id=1, name=value)
            db.session.add(new_loc)
            db.session.flush()
            item.location_id = new_loc.location_id

    else:  # name
        item.name = value

    db.session.commit()
    return jsonify(success=True)


@app.route('/program', methods=['GET', 'POST'])
def run_program():
    result = None
    if request.method == 'POST':
        days = int(request.form['x'])
        data = get_expiring_items(days)
        result = format_report(data)
        run = ProgramRun(input=str(days), output=result)
        db.session.add(run)
        db.session.commit()
    return render_template('program.html', result=result)


@app.route('/site-plan')
def site_plan():
    return render_template('site-plan.html')


@app.route('/contact-us')
def contact_us():
    return render_template('contactus.html')


if __name__ == '__main__':
    app.run(debug=True)
