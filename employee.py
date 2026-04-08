class Employee:
    def __init__(self, emp_id, name, role, salary):
        self.emp_id = emp_id
        self.name = name
        self.role = role
        self.salary = salary

    def display_info(self):
        return f"Employee ID: {self.emp_id}, Employee Name: {self.name}, Employee's Role: {self.role}, Employee's Salary: ${self.salary}"
