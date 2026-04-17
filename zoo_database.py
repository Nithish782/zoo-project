import sqlite3

class ZooDatabase:
    def __init__(self):
        self.conn = sqlite3.connect("zoo.db", check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.create_table()
        self.create_employee_table()
        self.create_visitor_table()
        self.create_ticket_table()
        self.create_feed_table()
        self.create_alert_table()
        self.alerts = []

    def create_table(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS animals (
            animal_id TEXT PRIMARY KEY,
            name TEXT,
            species TEXT,
            age INTEGER,
            health_status TEXT
        )
        """)
        self.conn.commit()

    def add_animal(self, animal):
        self.cursor.execute("INSERT INTO animals VALUES (?, ?, ?, ?, ?)",
            (animal.animal_id, animal.name, animal.species, animal.age, animal.health_status))
        self.conn.commit()

    def display_animals(self):
        self.cursor.execute("SELECT * FROM animals")
        return self.cursor.fetchall()

    def remove_animal(self, animal_id):
        self.cursor.execute("DELETE FROM animals WHERE animal_id=?", (animal_id,))
        self.conn.commit()
    
    def get_animal(self, animal_id):
        self.cursor.execute("SELECT * FROM animals WHERE animal_id=?", (animal_id,))
        return self.cursor.fetchone()

    def update_animal(self, animal_id, name, species, age, health):
        self.cursor.execute("""
        UPDATE animals 
        SET name=?, species=?, age=?, health_status=? 
        WHERE animal_id=?
        """, (name, species, age, health, animal_id))
        self.conn.commit()
    
    def search_animals(self, query):
        self.cursor.execute("""
        SELECT * FROM animals 
        WHERE name LIKE ? OR species LIKE ?
        """, (f'%{query}%', f'%{query}%'))
        return self.cursor.fetchall()
    
    def create_employee_table(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            emp_id TEXT PRIMARY KEY,
            name TEXT,
            role TEXT,
            salary REAL
        )
        """)
        self.conn.commit()

    def add_employee(self, emp):
        self.cursor.execute("INSERT INTO employees VALUES (?, ?, ?, ?)",
            (emp.emp_id, emp.name, emp.role, emp.salary))
        self.conn.commit()

    def get_employees(self):
        self.cursor.execute("SELECT * FROM employees")
        return self.cursor.fetchall()
    
    def delete_employee(self, emp_id):
        self.cursor.execute("DELETE FROM employees WHERE emp_id=?", (emp_id,))
        self.conn.commit()

    def get_employee(self, emp_id):
        self.cursor.execute("SELECT * FROM employees WHERE emp_id=?", (emp_id,))
        return self.cursor.fetchone()

    def update_employee(self, emp_id, name, role, salary):
        self.cursor.execute("""
        UPDATE employees
        SET name=?, role=?, salary=?
        WHERE emp_id=?
        """, (name, role, salary, emp_id))
        self.conn.commit()
    
    def create_visitor_table(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS visitors (
            visitor_id TEXT PRIMARY KEY,
            name TEXT,
            age INTEGER,
            ticket_id TEXT
        )
        """)
        self.conn.commit()

    def add_visitor(self, visitor):
        self.cursor.execute("INSERT INTO visitors VALUES (?, ?, ?, ?)",
            (visitor.visitor_id, visitor.name, visitor.age, visitor.ticket_id))
        self.conn.commit()

    def get_visitors(self):
        self.cursor.execute("SELECT * FROM visitors")
        return self.cursor.fetchall()
    
    def create_ticket_table(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS tickets (
            ticket_id TEXT PRIMARY KEY,
            price REAL,
            visitor_name TEXT
        )
        """)
        self.conn.commit()

    def add_ticket(self, ticket):
        self.cursor.execute("INSERT INTO tickets VALUES (?, ?, ?)",
            (ticket.ticket_id, ticket.price, ticket.visitor_name))
        self.conn.commit()

    def get_tickets(self):
        self.cursor.execute("SELECT * FROM tickets")
        return self.cursor.fetchall()
    
    def create_feed_table(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS feed_schedule (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            animal_id TEXT,
            time TEXT,
            food TEXT
        )
        """)
        self.conn.commit()

    def add_feed(self, animal_id, time, food):
        self.cursor.execute(
            "INSERT INTO feed_schedule (animal_id, time, food) VALUES (?, ?, ?)",
            (animal_id, time, food)
        )
        self.conn.commit()
    

    def create_alert_table(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            message TEXT,
            time TEXT
        )
        """)
        self.conn.commit()
    
    from datetime import datetime

    def add_alert(self, message):
        current_time = datetime.now().strftime("%H:%M:%S")

        self.cursor.execute(
            "INSERT INTO alerts (message, time) VALUES (?, ?)",
            (message, current_time)
        )
        self.conn.commit()
    
    

    def get_alerts(self):
        self.cursor.execute("SELECT * FROM alerts ORDER BY id DESC")
        return self.cursor.fetchall()

    def get_feed(self):
        self.cursor.execute("SELECT * FROM feed_schedule")
        return self.cursor.fetchall()
        