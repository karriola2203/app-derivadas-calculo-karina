import streamlit as st
import sympy as sp
import random

st.set_page_config(page_title="Cálculo Pro: Reglas de Derivación", layout="wide")

# --- LÓGICA DEL QUIZ ---
def generar_ejercicio():
    x = sp.symbols('x')
    a = random.randint(2, 6)
    # Funciones que invitan a usar reglas generalizadas
    opciones = [
        sp.exp(a*x),           # e^u
        sp.sin(x/a),           # sin(u)
        a*x**3 - (a-1)*x,      # Suma/Resta
        (x**2) * sp.exp(x),    # Producto
        x / (x + a)            # División
    ]
    f = random.choice(opciones)
    df = sp.diff(f, x)
    return f, df

if 'ejercicio' not in st.session_state:
    st.session_state.ejercicio, st.session_state.solucion = generar_ejercicio()

# --- INTERFAZ ---
st.title("🏛️ Tutorial de Técnicas de Derivación")
st.caption("Docente: Karina Arriola | Análisis de Estructuras")

tab1, tab2 = st.tabs(["📝 Solucionador Detallado", "🎮 Quiz de Técnicas"])

with tab1:
    st.header("Analizador de Reglas Aplicadas")
    u_f_text = st.text_input("Escribe la función a analizar:", "x * exp(x)")
    
    try:
        x = sp.symbols('x')
        f = sp.sympify(u_f_text.replace("^", "**"))
        
        st.markdown("### 🔍 Desglose de la Solución")
        
        # Identificación de la técnica
        if f.is_Add:
            regla = "Suma o Resta: \\frac{d}{dx}[u \pm v] = u' \pm v'"
        elif f.is_Mul and any(arg.has(x) for arg in f.args if len([a for a in f.args if a.has(x)]) > 1):
            regla = "Producto: \\frac{d}{dx}[u \\cdot v] = u'v + uv'"
        elif f.is_Pow and f.exp.is_constant:
            regla = "Potencia Generalizada: \\frac{d}{dx}[u^n] = n \\cdot u^{n-1} \\cdot u'"
        elif "exp" in str(f):
            regla = "Exponencial Generalizada: \\frac{d}{dx}[e^u] = e^u \\cdot u'"
        elif "sin" in str(f) or "cos" in str(f):
            regla = "Trigonométrica Generalizada: \\frac{d}{dx}[\\sin(u)] = \\cos(u) \\cdot u'"
        else:
            regla = "Regla Básica de Derivación"

        st.warning(f"*Regla a aplicar:* ${regla}$")
        
        # Mostrar el paso a paso simbólico
        st.write("1. *Identificamos los componentes:*")
        st.latex(f"f(x) = {sp.latex(f)}")
        
        st.write("2. *Aplicamos la técnica:*")
        pasos = sp.diff(f, x)
        st.latex(f"f'(x) = {sp.latex(pasos)}")
        
        st.success("*Resultado Simplificado:*")
        st.latex(f"f'(x) = {sp.latex(sp.simplify(pasos))}")

    except:
        st.error("Ingresa una función válida. Ejemplo: (x**2)/(x+1)")

with tab2:
    st.header("🎮 Practica las Técnicas")
    st.write("Calcula la derivada aplicando la regla correspondiente:")
    st.latex(f"f(x) = {sp.latex(st.session_state.ejercicio)}")
    
    ans = st.text_input("Tu respuesta f'(x):")
    
    if st.button("Validar"):
        try:
            u_ans = sp.sympify(ans.replace("^", "**"))
            if sp.simplify(u_ans - st.session_state.solucion) == 0:
                st.success("¡Excelente manejo de las reglas!")
                st.balloons()
            else:
                st.error("Revisa la aplicación de la regla. La solución es:")
                st.latex(sp.latex(st.session_state.solucion))
        except:
            st.warning("Formato no reconocido.")
    
    if st.button("Siguiente Reto"):
        st.session_state.ejercicio, st.session_state.solucion = generar_ejercicio()
        st.rerun()

# --- BARRA LATERAL EDUCATIVA ---
with st.sidebar:
    st.header("📋 Formulario de Referencia")
    st.latex(r"\frac{d}{dx}[u \cdot v] = u'v + uv'")
    st.latex(r"\frac{d}{dx}[\frac{u}{v}] = \frac{u'v - uv'}{v^2}")
    st.latex(r"\frac{d}{dx}[e^u] = e^u \cdot u'")
    st.latex(r"\frac{d}{dx}[\sin(u)] = \cos(u) \cdot u'")
