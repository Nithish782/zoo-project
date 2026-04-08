from animal import Animal
from employee import Employee
from visitor import Visitor
from feed_schedule import FeedSchedule
from ticket import Ticket
from zoo_database import ZooDatabase

def main():
    zoo_db = ZooDatabase()

    while True:
        print("\n===== ZOO MANAGEMENT SYSTEM =====")
        print("1. Add Animal")
        print("2. Add Employee")
        print("3. Add Visitor")
        print("4. Issue Ticket")
        print("5. View Animals")
        print("6. View Employees")
        print("7. View Visitors")
        print("8. Remove animals")
        print("9. Remove Employees")
        print("10. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            animal_id = input("Enter Animal ID: ")
            name = input("Enter Name: ")
            species = input("Enter Species: ")
            age = int(input("Enter Age: "))
            health_status = input("Enter Health Status: ")

            animal = Animal(animal_id, name, species, age, health_status)
            zoo_db.add_animal(animal)
            print("Animal Added Successfully!")

        elif choice == "2":
            emp_id = input("Enter Employee ID: ")
            name = input("Enter Name: ")
            role = input("Enter Role: ")
            salary = float(input("Enter Salary: "))

            employee = Employee(emp_id, name, role, salary)
            zoo_db.add_employee(employee)
            print("Employee Added Successfully!")

        elif choice == "3":
            visitor_id = input("Enter Visitor ID: ")
            name = input("Enter Name: ")
            age = int(input("Enter Age: "))
            ticket_id = input("Enter Ticket ID: ")

            visitor = Visitor(visitor_id, name, age, ticket_id)
            zoo_db.add_visitor(visitor)
            print("Visitor Added Successfully!")

        elif choice == "4":
            ticket_id = input("Enter Ticket ID: ")
            price = float(input("Enter Ticket Price: "))
            visitor_name = input("Enter Visitor Name: ")

            ticket = Ticket(ticket_id, price, visitor_name)
            zoo_db.add_ticket(ticket)
            print("Ticket Issued Successfully!")

        elif choice == "5":
            print("\n==== Animal List ====")
            for animal in zoo_db.display_animals():
                print(animal)

        elif choice == "6":
            print("\n==== Employee List ====")
            for employee in zoo_db.display_employees():
                print(employee)

        elif choice == "7":
            print("\n==== Visitor List ====")
            for visitor in zoo_db.display_visitors():
                print(visitor)

        elif choice == "8":
            print("\n=== Remove Animals ===")
            animal_id =input("Enter the animal id:")
            zoo_db.remove_animal(animal_id)
            print("Animal removed successfully!")
        
        elif choice == "9":
            print("\n=== Remove Employee ===")
            emp_id =input("Enter the Employee id:")
            zoo_db.remove_employee(emp_id)
            print("Person removed successfully!")

        elif choice == "10":
            print("Exiting Zoo Management System. Goodbye!")
            break

        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main()
