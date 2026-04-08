from flask import Flask, render_template, request, redirect, session
from zoo_database import ZooDatabase
from animal import Animal
import os

app = Flask(__name__)
app.secret_key = "zoo_secret"
zoo_db = ZooDatabase()

@app.route('/')
def home():
    if 'user' not in session:
        return redirect('/login')
    
    animals = len(zoo_db.display_animals())
    employees = len(zoo_db.get_employees())
    visitors = len(zoo_db.get_visitors())

    return render_template('index.html',
                           animals=animals,
                           employees=employees,
                           visitors=visitors)

# Add Animal Page
@app.route('/add_animal', methods=['GET', 'POST'])
def add_animal():
    if request.method == 'POST':
        animal_id = request.form['animal_id']
        name = request.form['name']
        species = request.form['species']
        age = int(request.form['age'])
        health_status = request.form['health_status']

        animal = Animal(animal_id, name, species, age, health_status)
        zoo_db.add_animal(animal)

        return redirect('/animals')

    return render_template('add_animal.html')

# View Animals
@app.route('/animals')
def view_animals():
    if 'user' not in session:
        return redirect('/login')
    
    animals = zoo_db.display_animals()
    return render_template('view_animals.html', animals=animals)



@app.route('/edit_animal/<id>', methods=['GET', 'POST'])
def edit_animal(id):
    if request.method == 'POST':
        zoo_db.update_animal(
            id,
            request.form['name'],
            request.form['species'],
            int(request.form['age']),
            request.form['health_status']
        )
        return redirect('/animals')

    animal = zoo_db.get_animal(id)
    return render_template('edit_animal.html', animal=animal)

@app.route('/search')
def search():
    query = request.args.get('q')
    animals = zoo_db.search_animals(query)
    return render_template('view_animals.html', animals=animals)

@app.route('/add_employee', methods=['GET','POST'])
def add_employee():
    if request.method == 'POST':
        from employee import Employee
        emp = Employee(
            request.form['emp_id'],
            request.form['name'],
            request.form['role'],
            float(request.form['salary'])
        )
        zoo_db.add_employee(emp)
        return redirect('/employees')

    return render_template('add_employee.html')

@app.route('/employees')
def employees():
    if 'user' not in session:
        return redirect('/login')
    
    emps = zoo_db.get_employees()
    return render_template('view_employees.html', employees=emps)

@app.route('/delete_employee/<id>')
def delete_employee(id):
    zoo_db.delete_employee(id)
    return redirect('/employees')

@app.route('/edit_employee/<id>', methods=['GET', 'POST'])
def edit_employee(id):
    if request.method == 'POST':
        zoo_db.update_employee(
            id,
            request.form['name'],
            request.form['role'],
            float(request.form['salary'])
        )
        return redirect('/employees')

    emp = zoo_db.get_employee(id)
    return render_template('edit_employee.html', emp=emp)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # simple login (you can improve later)
        if username == "admin" and password == "1234":
            session['user'] = username
            return redirect('/')
        else:
            return "Invalid Credentials"

    return render_template('login.html')

@app.route('/add_visitor', methods=['GET','POST'])
def add_visitor():
    if request.method == 'POST':
        from visitor import Visitor
        v = Visitor(
            request.form['visitor_id'],
            request.form['name'],
            int(request.form['age']),
            request.form['ticket_id']
        )
        zoo_db.add_visitor(v)
        return redirect('/visitors')

    return render_template('add_visitor.html')


@app.route('/visitors')
def visitors():
    data = zoo_db.get_visitors()
    return render_template('view_visitors.html', visitors=data)

@app.route('/add_ticket', methods=['GET','POST'])
def add_ticket():
    if request.method == 'POST':
        from ticket import Ticket
        t = Ticket(
            request.form['ticket_id'],
            float(request.form['price']),
            request.form['visitor_name']
        )
        zoo_db.add_ticket(t)
        return redirect('/tickets')

    return render_template('add_ticket.html')


@app.route('/tickets')
def tickets():
    data = zoo_db.get_tickets()
    return render_template('view_tickets.html', tickets=data)

@app.route('/add_feed', methods=['GET','POST'])
def add_feed():
    if request.method == 'POST':
        zoo_db.add_feed(
            request.form['animal_id'],
            request.form['time'],
            request.form['food']
        )
        return redirect('/feed')

    return render_template('add_feed.html')


@app.route('/feed')
def feed():
    data = zoo_db.get_feed()
    return render_template('view_feed.html', feed=data)

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/login')


if __name__ == "__main__":
     app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))