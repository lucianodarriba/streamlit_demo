import streamlit as st
import os
from dotenv import load_dotenv
from utils import logout, initialize_openai_client, authenticate_user, initialize_chat_history, display_chat_history, handle_user_input

# --- Configuración de la aplicación ---
st.title("🤖 Chat con Inteligencia Artificial")

# Inicializar cliente de OpenAI
initialize_openai_client()
client = st.session_state.openai_client

# Cargar variables de entorno
load_dotenv()

# Autenticación del usuario
PASSWORD = os.getenv("PASSWORD")
authenticate_user(PASSWORD)

# Mostrar botón de cierre de sesión
if st.session_state.authenticated:
    if st.button("Cerrar sesión"):
        logout()
        st.success("Sesión cerrada.")

# Inicializar y mostrar historial de conversación
initialize_chat_history()
display_chat_history()

# Manejar entrada del usuario
handle_user_input(client)