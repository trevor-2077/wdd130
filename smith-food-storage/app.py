from flask import Flask, render_template, request, redirect, url_for
from config import Config
from models import db, FoodItem, ProgramRun
from datetime import datetime
from student_program.core import compute_something, format_result

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

@app.before_first_request
def init_db():
    db.create_all()

@app.route('/')
def home():
    return redirect(url_for('add_food'))

@app.route('/add', methods=['GET','POST'])
def add_food():
    if request.method == 'POST':
        item = FoodItem(
            name=request.form['name'],
            quantity=int(request.form['quantity']),
            expires=datetime.strptime(request.form['expires'], '%Y-%m-%d'),
            location=request.form.get('location','')
        )
        db.session.add(item)
        db.session.commit()
        return redirect(url_for('storage'))
    return render_template('add.html')

@app.route('/storage')
def storage():
    items = FoodItem.query.order_by(FoodItem.expires).all()
    return render_template('storage.html', items=items)

@app.route('/program', methods=['GET','POST'])
def run_program():
    result = None
    if request.method == 'POST':
        x = int(request.form['x'])
        y = int(request.form['y'])
        raw = compute_something(x, y)
        result = format_result(raw)
        # Optional: save run
        rec = ProgramRun(input=f"{x},{y}", output=result)
        db.session.add(rec)
        db.session.commit()
    return render_template('program.html', result=result)

if __name__ == '__main__':
    app.run()
