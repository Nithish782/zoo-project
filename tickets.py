class Ticket:
    def __init__(self, ticket_id, price, visitor_name):
        self.ticket_id = ticket_id
        self.price = price
        self.visitor_name = visitor_name

    def display_info(self):
        return f"Ticket ID: {self.ticket_id}, Price: ${self.price}, Visitor: {self.visitor_name}"
