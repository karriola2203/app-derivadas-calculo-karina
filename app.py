import streamlit as st
import sympy as sp
import random

st.set_page_config(page_title="Profe de Mates: Reto Derivadas", layout="centered")

# --- LÓGICA DEL QUIZ ---
def generar_ejercicio():
    x = sp.symbols('x')
    # Lista de funciones base para el quiz
    n = random.randint(2, 5)
    a = random.randint(1, 10)
    funciones = [
        a * x**n,             # Ejemplo: 5x^3
        a * sp.sin(x),        # Ejemplo: 4sin(x)
        x**n + a*x,           # Ejemplo: x^2 + 5x
        sp.cos(a*x)           # Ejemplo: cos(3x)
    ]
    f = random.choice(funciones)
    df = sp.diff(f, x)
    return f, df

# Inicializar variables de estado para que no cambien al hacer clic
if 'ejercicio' not in st.session_state:
    st.session_state.ejercicio, st.session_state.solucion = generar_ejercicio()

# --- INTERFAZ ---
st.title("🎓 Academia de Derivadas")
tab1, tab2 = st.tabs(["🔍 Explorador Visual", "📝 Ponte a Prueba (Quiz)"])

with tab1:
    st.header("Visualiza la Pendiente")
    user_f = st.text_input("Escribe f(x):", "x**2", key="explorador")
    st.info("Usa el código anterior para ver la gráfica aquí. (Mantente enfocado en el Quiz abajo)")

with tab2:
    st.header("¿Cuánto sabes de derivadas?")
    st.write("Calcula la derivada de la siguiente función:")
    
    # Mostrar el problema en LaTeX
    st.latex(f"f(x) = {sp.latex(st.session_state.ejercicio)}")
    
    respuesta_usuario = st.text_input("Escribe f'(x) aquí:", key="quiz_input")
    
    col1, col2 = st.columns(2)
    
    if col1.button("Comprobar respuesta"):
        try:
            # Convertir respuesta del usuario a formato matemático
            user_df = sp.sympify(respuesta_usuario.replace("^", "**"))
            if sp.simplify(user_df - st.session_state.solucion) == 0:
                st.success("✨ ¡Excelente! Respuesta correcta.")
                st.balloons()
            else:
                st.error(f"Casi... la respuesta correcta era: {st.session_state.solucion}")
        except:
            st.warning("Asegúrate de escribir la función correctamente (ej. 2*x**2)")

    if col2.button("Siguiente ejercicio ➡️"):
        st.session_state.ejercicio, st.session_state.solucion = generar_ejercicio()
        st.rerun()

st.sidebar.markdown("---")
st.sidebar.write("👩‍🏫 *Consejo de la Profe:*")
st.sidebar.write("Recuerda que la derivada de una constante siempre es 0 y la de $x^n$ es $nx^{n-1}$.")
