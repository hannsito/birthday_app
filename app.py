import streamlit as st
import pickle
import datetime
import os
import random
import smtplib
import ssl

# Función para cargar los cumpleaños desde un archivo PICKLE
def load_birthdays():
    if os.path.exists('birthdays.pkl'):
        with open('birthdays.pkl', 'rb') as f:
            return pickle.load(f)
    else:
        return {}

# Función para guardar los cumpleaños en un archivo PICKLE
def save_birthdays(birthdays):
    with open('birthdays.pkl', 'wb') as f:
        pickle.dump(birthdays, f)

# Función para calcular días hasta el próximo cumpleaños
def days_until_birthday(birthday):
    today = datetime.date.today()
    next_birthday = birthday.replace(year=today.year)
    if next_birthday < today:
        next_birthday = next_birthday.replace(year=today.year + 1)
    return (next_birthday - today).days

# Función para enviar un mensaje de felicitación
def send_birthday_message(email, message):
    port = 587  # Puerto para STARTTLS
    smtp_server = "smtp.gmail.com"
    sender_email = "sua.parra@ALUMNOS.UDG.MX"  # Tu correo de origen
    password = "zfkw nhjt jrsu wbyw"  # La contraseña de aplicación generada

    full_message = f"""\
Subject: ¡Feliz Cumpleaños!

{message}"""

    context = ssl.create_default_context()
    try:
        with smtplib.SMTP(smtp_server, port) as server:
            server.ehlo()  # Puede omitirse
            server.starttls(context=context)
            server.ehlo()  # Puede omitirse
            server.login(sender_email, password)
            server.sendmail(sender_email, email, full_message.encode('utf-8'))
            st.success(f"Mensaje enviado a {email}: {message}")
    except Exception as e:
        st.error(f"Error al enviar el mensaje a {email}: {e}")

# Interfaz de usuario
st.title("Recordatorio de Cumpleaños")

# Registro de cumpleaños
st.header("Registrar Cumpleaños")
name = st.text_input("Nombre")
birthday = st.date_input("Fecha de Nacimiento")
email = st.text_input("Correo Electrónico")
message_options = st.text_area("Mensajes de Felicitación (separados por comas)", "¡Feliz cumpleaños!, ¡Que tengas un gran día!")

if st.button("Registrar"):
    birthdays = load_birthdays()
    if name and birthday and email:
        birthdays[name] = {'birthday': birthday, 'email': email, 'messages': message_options.split(',')}
        save_birthdays(birthdays)
        st.success(f"Cumpleaños de {name} registrado.")
    else:
        st.error("Por favor, completa todos los campos.")

# Mostrar próximos cumpleaños
st.header("Próximos Cumpleaños")
birthdays = load_birthdays()
today = datetime.date.today()

for name, info in birthdays.items():
    birthday = info['birthday']
    days_left = days_until_birthday(birthday)
    email = info['email']
    
    if days_left == 0:
        st.write(f"🎉 ¡Hoy es el cumpleaños de {name}! 🎉")
        message = random.choice(info['messages']).strip()
        send_birthday_message(email, message)
    else:
        st.write(f"{name}: {days_left} días hasta su cumpleaños.")