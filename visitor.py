class Visitor:
    def __init__(self, visitor_id, name, age, ticket_id):
        self.visitor_id = visitor_id
        self.name = name
        self.age = age
        self.ticket_id = ticket_id

    def display_info(self):
        return f"Visitor ID: {self.visitor_id}, Visitor Name: {self.name}, Visitor's Age: {self.age}, Ticket ID: {self.ticket_id}"
