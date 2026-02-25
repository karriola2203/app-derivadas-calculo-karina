import streamlit as st
import sympy as sp
import numpy as np

st.set_page_config(page_title="Cátedra Arriola: Análisis de Derivadas", layout="wide")

st.title("🏛️ Tutor de Derivación Detallada")
st.subheader("Facultad de Arquitectura | Profe Karina Arriola")

# --- ENTRADA ---
u_input = st.text_input("Ingresa la función para desglosar paso a paso:", "x**2 * sin(x)")

try:
    x = sp.symbols('x')
    h = sp.sympify(u_input.replace("^", "**"))
    
    st.markdown("---")
    st.write("### 🔍 Desglose de la Solución")

    # --- LÓGICA DE IDENTIFICACIÓN ---
    # CASO PRODUCTO
    if h.is_Mul and len([arg for arg in h.args if arg.has(x)]) > 1:
        args = [arg for arg in h.args if arg.has(x)]
        f = args[0]
        g = sp.Mul(*args[1:])
        df = sp.diff(f, x)
        dg = sp.diff(g, x)
        
        st.info("*Regla Identificada:* Regla del Producto")
        st.latex(r"\text{Técnica: } [f(x) \cdot g(x)]' = f'(x)g(x) + f(x)g'(x)")
        
        col1, col2 = st.columns(2)
        with col1:
            st.write("*Componentes:*")
            st.latex(f"f(x) = {sp.latex(f)}")
            st.latex(f"g(x) = {sp.latex(g)}")
        with col2:
            st.write("*Derivadas individuales:*")
            st.latex(f"f'(x) = {sp.latex(df)}")
            st.latex(f"g'(x) = {sp.latex(dg)}")
            
        st.write("*Ensamblaje de la solución:*")
        st.latex(f"h'(x) = ({sp.latex(df)}) \cdot ({sp.latex(g)}) + ({sp.latex(f)}) \cdot ({sp.latex(dg)})")

    # CASO COCIENTE
    elif h.is_Pow and h.exp.is_negative or " / " in u_input or isinstance(h, sp.core.mul.Mul) and any(isinstance(arg, sp.core.power.Pow) and arg.exp.is_negative for arg in h.args):
        # Simplificación para detectar cociente
        num, den = sp.fraction(h)
        f = num
        g = den
        df = sp.diff(f, x)
        dg = sp.diff(g, x)

        st.info("*Regla Identificada:* Regla del Cociente")
        st.latex(r"\text{Técnica: } \left[\frac{f(x)}{g(x)}\right]' = \frac{f'(x)g(x) - f(x)g'(x)}{[g(x)]^2}")
        
        col1, col2 = st.columns(2)
        with col1:
            st.write("*Componentes:*")
            st.latex(f"f(x) = {sp.latex(f)}")
            st.latex(f"g(x) = {sp.latex(g)}")
        with col2:
            st.write("*Derivadas individuales:*")
            st.latex(f"f'(x) = {sp.latex(df)}")
            st.latex(f"g'(x) = {sp.latex(dg)}")

        st.write("*Ensamblaje de la solución:*")
        st.latex(f"h'(x) = \\frac{({sp.latex(df)})({sp.latex(g)}) - ({sp.latex(f)})({sp.latex(dg)})}{({sp.latex(g)})^2}")

    # CASO FUNCIÓN GENERALIZADA (Seno, Coseno, Exponencial)
    elif any(func in str(h) for func in ["sin", "cos", "exp"]):
        # Extraemos el argumento interno como g(x)
        main_func = h.func
        g = h.args[0]
        dg = sp.diff(g, x)
        
        if "exp" in str(h):
            st.info("*Regla Identificada:* Exponencial Generalizada")
            st.latex(r"\text{Técnica: } [e^{g(x)}]' = e^{g(x)} \cdot g'(x)")
            f_expr = "e^{g(x)}"
        elif "sin" in str(h):
            st.info("*Regla Identificada:* Trigonométrica (Seno) Generalizada")
            st.latex(r"\text{Técnica: } [\sin(g(x))]' = \cos(g(x)) \cdot g'(x)")
            f_expr = r"\sin(g(x))"
        else:
            st.info("*Regla Identificada:* Trigonométrica (Coseno) Generalizada")
            st.latex(r"\text{Técnica: } [\cos(g(x))]' = -\sin(g(x)) \cdot g'(x)")
            f_expr = r"\cos(g(x))"

        st.write("*Identificación:*")
        st.latex(f"g(x) = {sp.latex(g)} \\implies g'(x) = {sp.latex(dg)}")
        st.write("*Aplicando la técnica:*")
        resultado_paso = sp.diff(h, x)
        st.latex(f"h'(x) = {sp.latex(resultado_paso)}")

    else:
        st.info("*Regla Identificada:* Regla de la Potencia / Suma")
        st.write("Se aplica la derivada término a término.")
        st.latex(f"h'(x) = {sp.latex(sp.diff(h, x))}")

    # RESULTADO FINAL
    st.success("### ✅ Resultado Simplificado Final")
    st.latex(f"h'(x) = {sp.latex(sp.simplify(sp.diff(h, x)))}")

except Exception as e:
    st.error("Error al procesar la función. Asegúrate de usar '*' para multiplicar (ej. 5*x).")

# --- BARRA LATERAL ---
with st.sidebar:
    st.header("📖 Glosario de Técnicas")
    st.write("*Regla del Producto:* Para funciones que se multiplican.")
    st.write("*Regla del Cociente:* Para funciones en fracción.")
    st.write("*Función Generalizada:* Cuando el argumento no es simplemente 'x'.")
