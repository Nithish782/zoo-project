from flask import Flask, render_template, request, redirect, session, Response
from zoo_database import ZooDatabase
from animal import Animal
import time
from ai_monitor import generate_frames

app = Flask(__name__)
app.secret_key = "zoo_secret"

zoo_db = ZooDatabase()


# -------------------- HOME --------------------
@app.route('/')
def home():
    if 'user' not in session:
        return redirect('/login')

    return render_template(
        'index.html',
        animals=len(zoo_db.display_animals()),
        employees=len(zoo_db.get_employees()),
        visitors=len(zoo_db.get_visitors())
    )


# -------------------- ANIMALS (COMBINED) --------------------
@app.route('/animals', methods=['GET', 'POST'])
def view_animals():
    if 'user' not in session:
        return redirect('/login')

    if request.method == 'POST':
        animal = Animal(
            request.form['animal_id'],
            request.form['name'],
            request.form['species'],
            int(request.form['age']),
            request.form['health_status']
        )
        zoo_db.add_animal(animal)
        return redirect('/animals')

    animals = zoo_db.display_animals()
    return render_template('view_animals.html', animals=animals)


@app.route('/delete_animal/<animal_id>')
def delete_animal(animal_id):
    zoo_db.remove_animal(animal_id)
    return redirect('/animals')

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


# -------------------- EMPLOYEES (COMBINED) --------------------
@app.route('/employees', methods=['GET', 'POST'])
def employees():
    if 'user' not in session:
        return redirect('/login')

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

    data = zoo_db.get_employees()
    return render_template('view_employees.html', employees=data)


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

@app.route('/delete_employee/<id>')
def delete_employee(id):
    zoo_db.delete_employee(id)
    return redirect('/employees')


# -------------------- VISITORS (COMBINED) --------------------
@app.route('/visitors', methods=['GET', 'POST'])
def visitors():
    if 'user' not in session:
        return redirect('/login')

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

    data = zoo_db.get_visitors()
    return render_template('view_visitors.html', visitors=data)

@app.route('/edit_visitor/<id>', methods=['GET', 'POST'])
def edit_visitor(id):
    if request.method == 'POST':
        zoo_db.update_visitor(
            id,
            request.form['name'],
            int(request.form['age']),
            request.form['ticket_id']
        )
        return redirect('/visitors')

    visitor = zoo_db.get_visitor(id)
    return render_template('edit_visitor.html', visitor=visitor)

@app.route('/delete_visitor/<id>')
def delete_visitor(id):
    zoo_db.delete_visitor(id)
    return redirect('/visitors')


# -------------------- TICKETS (COMBINED) --------------------
@app.route('/tickets', methods=['GET', 'POST'])
def tickets():
    if request.method == 'POST':
        from models.ticket import Ticket

        ticket = Ticket(
            request.form['ticket_id'],
            float(request.form['price']),
            request.form['visitor_name']
        )
        zoo_db.add_ticket(ticket)
        return redirect('/tickets')

    data = zoo_db.get_tickets()
    return render_template('view_tickets.html', tickets=data)

@app.route('/edit_ticket/<id>', methods=['GET', 'POST'])
def edit_ticket(id):
    if request.method == 'POST':
        zoo_db.update_ticket(
            id,
            float(request.form['price']),
            request.form['visitor_name']
        )
        return redirect('/tickets')

    ticket = zoo_db.get_ticket(id)
    return render_template('edit_ticket.html', ticket=ticket)

@app.route('/delete_ticket/<id>')
def delete_ticket(id):
    zoo_db.delete_ticket(id)
    return redirect('/tickets')

# -------------------- FEED (COMBINED) --------------------
@app.route('/feed', methods=['GET', 'POST'])
def feed():
    if request.method == 'POST':
        zoo_db.add_feed(
            request.form['animal_id'],
            request.form['time'],
            request.form['food']
        )
        return redirect('/feed')

    data = zoo_db.get_feed()
    return render_template('view_feed.html', feed=data)

@app.route('/edit_feed/<int:id>', methods=['GET', 'POST'])
def edit_feed(id):
    if request.method == 'POST':
        zoo_db.update_feed(
            id,
            request.form['animal_id'],
            request.form['time'],
            request.form['food']
        )
        return redirect('/feed')

    feed = zoo_db.get_feed_by_id(id)
    return render_template('edit_feed.html', feed=feed)

@app.route('/delete_feed/<id>')
def delete_feed(id):
    zoo_db.delete_feed(id)
    return redirect('/feed')


# -------------------- ALERTS --------------------
@app.route('/alerts')
def alerts():
    data = zoo_db.get_alerts()
    return render_template('alerts.html', alerts=data)


@app.route('/add_alert', methods=['POST'])
def add_alert():
    data = request.get_json()

    zoo_db.add_alert(
        data.get("message"),
        time.strftime("%Y-%m-%d %H:%M:%S")
    )

    return {"status": "ok"}, 200


# -------------------- AI MONITOR --------------------
@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/live')
def live():
    return render_template("ai_monitor.html")


# -------------------- LOGIN --------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] == "admin" and request.form['password'] == "1234":
            session['user'] = "admin"
            return redirect('/')
        return "Invalid Credentials"

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/login')


if __name__ == "__main__":
    app.run(debug=True)