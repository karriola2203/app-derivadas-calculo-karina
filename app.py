import streamlit as st
import sympy as sp

# Configuración de la página
st.set_page_config(page_title="Cátedra Arriola: Tutor de Derivadas", layout="wide")

# --- BARRA LATERAL (LEYENDA DE SÍMBOLOS) ---
with st.sidebar:
    st.header("⌨️ Guía de Escritura")
    st.markdown("""
    Para que el tutor entienda tu función, usa estos símbolos:
    
    * **`*` (Asterisco):** Obligatorio para multiplicar. 
        * Ejemplo: `5*x` (en lugar de 5x)
    * **`^` o `**`:** Para potencias.
        * Ejemplo: `x^2` o `x**2`
    * **`/` (Barra):** Para fracciones.
        * Ejemplo: `(x+1)/x`
    * **`()` (Paréntesis):** Para agrupar argumentos.
        * Ejemplo: `sin(3*x)`
    
    ---
    **Ejemplos de formas generales:**
    * `sin(5*x)`
    * `cos(2*x)`
    * `exp(4*x)` o `e^(4*x)`
    """)
    st.info("💡 Consejo: Siempre pon el `*` entre el número y la `x`.")

st.title("🏛️ Tutor de Derivación Detallada")
st.subheader("Facultad de Arquitectura | Profe Karina Arriola")

# --- BLOQUE 1: EDITOR CON VISTA PREVIA ---
st.write("### ✍️ Editor de Funciones")
col_input, col_preview = st.columns([1, 1])

with col_input:
    u_input = st.text_input("Digita tu función aquí:", value="sin(3*x)")

x = sp.symbols('x')

try:
    # PRE-PROCESAMIENTO: Aceptamos '^', 'e^' y los convertimos a formato SymPy
    input_procesado = u_input.replace("^", "**").replace("e**", "exp")
    h = sp.sympify(input_procesado)
    
    with col_preview:
        st.markdown("#### 👁️ Interpretación Matemática:")
        st.latex(f"f(x) = {sp.latex(h)}")

except Exception as e:
    with col_preview:
        st.error("⚠️ Error de escritura. Revisa la guía de la izquierda.")
    st.stop()

st.markdown("---")

# --- BLOQUE 2: DESGLOSE DE SOLUCIÓN ---
if h:
    st.write("### 🔍 Desglose de la Solución")

    # 1. PRODUCTO
    if h.is_Mul and len([arg for arg in h.args if arg.has(x)]) > 1:
        args = [arg for arg in h.args if arg.has(x)]
        f = args[0]
        g = sp.Mul(*args[1:])
        df = sp.diff(f, x)
        dg = sp.diff(g, x)
        
        st.markdown("#### **Técnica: Regla del Producto**")
        st.latex(r"[f(x) \cdot g(x)]' = f'(x)g(x) + f(x)g'(x)")
        
        c1, c2 = st.columns(2)
        with c1:
            st.write("*Componentes:*")
            st.latex(f"f(x) = {sp.latex(f)}")
            st.latex(f"g(x) = {sp.latex(g)}")
        with c2:
            st.write("*Derivadas:*")
            st.latex(f"f'(x) = {sp.latex(df)}")
            st.latex(f"g'(x) = {sp.latex(dg)}")
            
        st.write("*Ensamblaje:*")
        st.latex(f"h'(x) = ({sp.latex(df)})({sp.latex(g)}) + ({sp.latex(f)})({sp.latex(dg)})")

    # 2. COCIENTE
    elif sp.fraction(h)[1] != 1:
        num, den = sp.fraction(h)
        f, g = num, den
        df, dg = sp.diff(f, x), sp.diff(g, x)

        st.markdown("#### **Técnica: Regla del Cociente**")
        st.latex(r"\left[\frac{f(x)}{g(x)}\right]' = \frac{f'(x)g(x) - f(x)g'(x)}{[g(x)]^2}")
        
        c1, c2 = st.columns(2)
        with c1:
            st.write("*Componentes:*")
            st.latex(f"f(x) = {sp.latex(f)}")
            st.latex(f"g(x) = {sp.latex(g)}")
        with c2:
            st.write("*Derivadas:*")
            st.latex(f"f'(x) = {sp.latex(df)}")
            st.latex(f"g'(x) = {sp.latex(dg)}")

        st.write("*Ensamblaje:*")
        st.latex(f"h'(x) = \\frac{({sp.latex(df)})({sp.latex(g)}) - ({sp.latex(f)})({sp.latex(dg)})}{({sp.latex(g)})^2}")

    # 3. FORMAS GENERALES (sin, cos, exp)
    elif any(func_name in str(h) for func_name in ["sin", "cos", "exp"]):
        arg = h.args[0]
        a = sp.diff(arg, x)
        
        if "exp" in str(h):
            st.markdown("#### **Técnica: Exponencial de forma general $e^{ax}$**")
            st.latex(r"[e^{ax}]' = a \cdot e^{ax}")
        elif "sin" in str(h):
            st.markdown("#### **Técnica: Seno de forma general $\sin(ax)$**")
            st.latex(r"[\sin(ax)]' = a \cdot \cos(ax)")
        elif "cos" in str(h):
            st.markdown("#### **Técnica: Coseno de forma general $\cos(ax)$**")
            st.latex(r"[\cos(ax)]' = -a \cdot \sin(ax)")

        st.write(f"Identificamos que el coeficiente es $a = {sp.latex(a)}$")
        st.write("*Aplicando la forma general:*")
        st.latex(f"h'(x) = {sp.latex(sp.diff(h, x))}")

    # 4. POTENCIA / SUMA
    else:
        st.markdown("#### **Técnica: Potencia / Suma Directa**")
        st.latex(f"h'(x) = {sp.latex(sp.diff(h, x))}")

    # --- RESULTADO FINAL ---
    st.markdown("---")
    st.success("### ✅ Resultado Simplificado Final")
    st.latex(f"h'(x) = {sp.latex(sp.simplify(sp.diff(h, x)))}")
