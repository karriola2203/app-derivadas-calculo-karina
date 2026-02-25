import streamlit as st
import sympy as sp
import random

st.set_page_config(page_title="Profe Karina: Derivadas Paso a Paso", layout="centered")

# --- LÓGICA DEL QUIZ (Funciones tipo Arquitectura) ---
def generar_ejercicio():
    x = sp.symbols('x')
    a = random.randint(2, 5)
    # Mezclamos polinómicas, exponenciales y trigonométricas
    tipo = random.choice(['poly', 'exp', 'sin', 'cos'])
    
    if tipo == 'poly':
        f = a * x**random.randint(2, 4)
    elif tipo == 'exp':
        f = sp.exp(a * x)
    elif tipo == 'sin':
        f = sp.sin(x / a)
    else:
        f = sp.cos(a * x)
        
    df = sp.diff(f, x)
    return f, df

# Inicializar estados
if 'ejercicio' not in st.session_state:
    st.session_state.ejercicio, st.session_state.solucion = generar_ejercicio()
if 'aciertos' not in st.session_state:
    st.session_state.aciertos = 0

# --- INTERFAZ ---
st.title("🎓 Academia de Derivadas")
st.subheader("Facultad de Arquitectura | Profe: Karina Arriola")

tab1, tab2 = st.tabs(["🔍 Calculadora Paso a Paso", "📝 Quiz con Calificación"])

with tab1:
    st.header("Analizador de Derivadas")
    st.write("Escribe una función para ver su derivada explicada.")
    
    user_f_raw = st.text_input("Ingresa f(x):", "exp(3*x)", help="Usa exp(x) para e^x, sin(x) para seno y cos(x) para coseno.")
    
    try:
        x = sp.symbols('x')
        # Limpieza de entrada
        f_user = sp.sympify(user_f_raw.replace("^", "**"))
        df_user = sp.diff(f_user, x)
        
        st.markdown("### 📝 Desarrollo:")
        st.write("1. *Función original identificada:*")
        st.latex(f"f(x) = {sp.latex(f_user)}")
        
        st.write("2. *Aplicando reglas de derivación:*")
        # Aquí mostramos el resultado directo, pero formateado
        st.latex(f"\\frac{{d}}{{dx}}[{sp.latex(f_user)}]")
        
        st.success("*Resultado Final:*")
        st.latex(f"f'(x) = {sp.latex(df_user)}")
        
    except:
        st.error("Error en el formato. Ejemplo: 5*x**2 o exp(2*x)")

with tab2:
    st.header("¿Cuánto sabes de derivadas?")
    
    # Marcador de calificación
    st.sidebar.metric("Aciertos Totales", st.session_state.aciertos)
    
    st.write("Calcula la derivada de la siguiente función:")
    st.latex(f"f(x) = {sp.latex(st.session_state.ejercicio)}")
    
    respuesta_usuario = st.text_input("Escribe tu respuesta f'(x):", key="quiz_input")
    
    col1, col2 = st.columns(2)
    
    if col1.button("Comprobar respuesta"):
        try:
            # Convertir respuesta a Sympy para comparar lógicamente
            user_df = sp.sympify(respuesta_usuario.replace("^", "**"))
            if sp.simplify(user_df - st.session_state.solucion) == 0:
                st.success("✨ ¡Excelente! Respuesta correcta.")
                st.session_state.aciertos += 1
                st.balloons()
            else:
                st.error(f"Casi... La respuesta correcta era:")
                st.latex(sp.latex(st.session_state.solucion))
        except:
            st.warning("Usa el formato matemático correcto (ej. 3*exp(3*x) o 2*x)")

    if col2.button("Siguiente ejercicio ➡️"):
        st.session_state.ejercicio, st.session_state.solucion = generar_ejercicio()
        st.rerun()

st.sidebar.markdown("---")
st.sidebar.write("👩‍🏫 *Consejo de Karina:*")
st.sidebar.info("Para funciones compuestas como $e^{ax}$, recuerda la regla de la cadena: la derivada es $a \\cdot e^{ax}$.")
