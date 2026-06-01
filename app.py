from flask import Flask, render_template, request, redirect, url_for
from models import db, Task

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = (
    'mysql+mysqlconnector://root:root@localhost/todo'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app) 

with app.app_context():
    db.create_all()

# 🔹 RETRIEVE
@app.route('/')
def index():
    tasks = Task.query.all()
    return render_template('index.html', tasks=tasks)

# 🔹 CREATE
@app.route('/add', methods=['POST'])
def add():
    name = request.form['name']
    description = request.form['description']
    status = request.form['status']

    task = Task(name=name, description=description, status=status)
    db.session.add(task)
    db.session.commit()
    return redirect(url_for('index'))

# 🔹 UPDATE (Show edit page)
@app.route('/edit/<int:id>')
def edit(id):
    task = Task.query.get_or_404(id)
    return render_template('edit.html', task=task)

# 🔹 UPDATE (Save changes)
@app.route('/update/<int:id>', methods=['POST'])
def update(id):
    task = Task.query.get_or_404(id)
    task.name = request.form['name']
    task.description = request.form['description']
    task.status = request.form['status']

    db.session.commit()
    return redirect(url_for('index'))

# 🔹 DELETE
@app.route('/delete/<int:id>')
def delete(id):
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
