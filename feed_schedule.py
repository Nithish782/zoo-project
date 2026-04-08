class FeedSchedule:
    def __init__(self, schedule_id, animal_id, feeding_time, food_type):
        self.schedule_id = schedule_id
        self.animal_id = animal_id
        self.feeding_time = feeding_time
        self.food_type = food_type

    def display_info(self):
        return f"Schedule ID: {self.schedule_id}, Animal ID: {self.animal_id}, Time: {self.feeding_time}, Food: {self.food_type}"
