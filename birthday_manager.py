import csv
import pickle
from datetime import datetime, timedelta
from email_sender import EmailSender
from random import choice

class BirthdayManager:
    def __init__(self, storage_file='data.pkl', use_pickle=True):
        self.storage_file = storage_file
        self.use_pickle = use_pickle
        self.birthdays = self.load_data()

    def load_data(self):
        try:
            if self.use_pickle:
                with open(self.storage_file, 'rb') as f:
                    return pickle.load(f)
            else:
                with open(self.storage_file, 'r') as f:
                    reader = csv.reader(f)
                    return {row[0]: {'email': row[1], 'birthday': row[2]} for row in reader}
        except FileNotFoundError:
            return {}

    def save_data(self):
        if self.use_pickle:
            with open(self.storage_file, 'wb') as f:
                pickle.dump(self.birthdays, f)
        else:
            with open(self.storage_file, 'w', newline='') as f:
                writer = csv.writer(f)
                for name, info in self.birthdays.items():
                    writer.writerow([name, info['email'], info['birthday']])

    def add_birthday(self, name, email, birthday):
        self.birthdays[name] = {'email': email, 'birthday': birthday}
        self.save_data()

    def get_upcoming_birthdays(self):
        today = datetime.today()
        upcoming = []
        for name, info in self.birthdays.items():
            bday = datetime.strptime(info['birthday'], '%Y-%m-%d')
            next_bday = bday.replace(year=today.year) if bday.replace(year=today.year) > today else bday.replace(year=today.year + 1)
            days_left = (next_bday - today).days
            upcoming.append((name, days_left))
        return sorted(upcoming, key=lambda x: x[1])

    def send_greeting(self, name, message_manager):
        email = self.birthdays[name]['email']
        message = message_manager.get_random_message(name)
        EmailSender().send_email(email, message)
