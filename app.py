import streamlit as st
from birthday_manager import BirthdayManager
from message_manager import MessageManager

st.title("Registro de Cumpleaños")

manager = BirthdayManager()
message_manager = MessageManager()

st.header("Registrar Nuevo Cumpleaños")
name = st.text_input("Nombre")
email = st.text_input("Email")
birthday = st.date_input("Fecha de Nacimiento")

if st.button("Registrar"):
    manager.add_birthday(name, email, birthday.strftime('%Y-%m-%d'))
    st.success("¡Cumpleaños registrado exitosamente!")

st.header("Próximos Cumpleaños")
upcoming_birthdays = manager.get_upcoming_birthdays()
for name, days_left in upcoming_birthdays:
    st.write(f"{name}: {days_left} días para el próximo cumpleaños")
