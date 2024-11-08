import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class EmailSender:
    def __init__(self, smtp_server='smtp.example.com', smtp_port=587, username='your_email@example.com', password='password'):
        self.server = smtp_server
        self.port = smtp_port
        self.username = username
        self.password = password

    def send_email(self, recipient_email, message):
        msg = MIMEMultipart()
        msg['From'] = self.username
        msg['To'] = recipient_email
        msg['Subject'] = "¡Feliz Cumpleaños!"
        msg.attach(MIMEText(message, 'plain'))
        
        with smtplib.SMTP(self.server, self.port) as server:
            server.starttls()
            server.login(self.username, self.password)
            server.send_message(msg)
