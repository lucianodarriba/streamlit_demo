import streamlit as st
from openai import OpenAI
import os

# --- Funciones auxiliares ---
def logout():
    """
    Cierra la sesión del usuario, limpia el historial de mensajes y recarga la aplicación.
    """
    st.session_state.authenticated = False
    st.session_state.messages = []
    st.rerun()

def initialize_openai_client():
    """
    Inicializa el cliente de OpenAI utilizando la clave API desde las variables de entorno.
    """
    if "openai_client" not in st.session_state:
        openai_api_key = os.getenv("OPENAI_API_KEY")
        if not openai_api_key:
            st.error("La clave API de OpenAI no está configurada.")
            st.stop()
        st.session_state.openai_client = OpenAI(api_key=openai_api_key)

def authenticate_user(password):
    """
    Autentica al usuario mediante una contraseña simple.
    """
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        pwd = st.text_input("Ingresá la contraseña para acceder:", type="password")
        if pwd == password:
            st.session_state.authenticated = True
            st.success("Acceso concedido.")
        else:
            st.error("Contraseña incorrecta. Intenta nuevamente.")
            st.stop()

def initialize_chat_history():
    """
    Inicializa el historial de conversación con un mensaje del sistema.
    """
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "system", "content": "Sos un asistente útil y amable."}
        ]

def display_chat_history():
    """
    Muestra el historial de mensajes en la interfaz de usuario.
    """
    for msg in st.session_state.messages[1:]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

def handle_user_input(client):
    """
    Procesa el mensaje del usuario, llama a la API de OpenAI y muestra la respuesta.
    """
    user_input = st.chat_input("Escribí tu mensaje...")
    if user_input:
        # Mostrar el mensaje del usuario
        st.chat_message("user").markdown(user_input)
        st.session_state.messages.append({"role": "user", "content": user_input})

        # Llamar a la API de OpenAI
        with st.spinner("Pensando..."):
            try:
                response = client.responses.create(
                    model="gpt-4o-mini",
                    input=st.session_state.messages
                )
                reply = response.output_text
            except Exception as e:
                st.error(f"Error al comunicarse con OpenAI: {e}")
                return

        # Mostrar la respuesta
        st.chat_message("assistant").markdown(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})