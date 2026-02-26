import streamlit as st
import sympy as sp

# Configuración de la página
st.set_page_config(page_title="Cátedra Arriola: Tutor de Derivadas", layout="wide")

# --- BARRA LATERAL (GUÍA DE APOYO) ---
with st.sidebar:
    st.header("⌨️ Guía para el Alumno")
    st.markdown("""
    **Operadores:**
    * `*` : Multiplicación
    * `^` : Potencia
    * `/` : División
    
    **Ejemplos para practicar:**
    1. `(x^2 + 1) / (x - 1)`
    2. `x^3 * sin(4*x)`
    3. `exp(2*x) - cos(5*x)`
    """)
    st.info("Cada paso mostrará la fórmula aplicada antes del resultado.")

st.title("🏛️ Tutor de Derivación Detallada")
st.subheader("Facultad de Arquitectura | Profe Karina Arriola")

# --- BLOQUE 1: EDITOR Y VISTA PREVIA ---
st.write("### ✍️ Editor de Funciones")
col_input, col_preview = st.columns([1, 1])

with col_input:
    u_input = st.text_input("Ingresa tu función:", value="x^2 / sin(3*x)")

x = sp.symbols('x')

try:
    input_proc = u_input.replace("^", "**").replace("e**", "exp")
    h = sp.sympify(input_proc)
    with col_preview:
        st.markdown("#### 👁️ Interpretación Matemática:")
        st.latex(f"f(x) = {sp.latex(h)}")
except Exception:
    st.error("⚠️ Error en la escritura. Revisa los asteriscos (*) y paréntesis.")
    st.stop()

st.markdown("---")

# --- BLOQUE 2: DESARROLLO PEDAGÓGICO ---
if h:
    st.write("### 🔍 Procedimiento de Derivación")
    
    terminos = sp.Add.make_args(h)
    
    for i, t in enumerate(terminos):
        st.write(f"#### **Análisis del Término {i+1}:**")
        st.latex(f"f_{i+1}(x) = {sp.latex(t)}")

        # --- CASO A: DIVISIÓN (COCIENTE) ---
        num, den = sp.fraction(t)
        if den != 1 and den.has(x):
            st.warning("📐 **Técnica Detectada: Regla del Cociente**")
            st.write("Se aplica la fórmula para funciones racionales:")
            st.latex(r"\frac{d}{dx} \left[ \frac{u}{v} \right] = \frac{u' \cdot v - u \cdot v'}{v^2}")
            
            
            u, v = num, den
            du, dv = sp.diff(u, x), sp.diff(v, x)
            
            st.write("**Paso 1: Identificar componentes y sus derivadas:**")
            c1, c2 = st.columns(2)
            with c1:
                st.latex(f"u = {sp.latex(u)} \implies u' = {sp.latex(du)}")
            with c2:
                st.latex(f"v = {sp.latex(v)} \implies v' = {sp.latex(dv)}")
            
            st.write("**Paso 2: Sustituir en la fórmula:**")
            st.latex(f"\\frac{{({sp.latex(du)})({sp.latex(v)}) - ({sp.latex(u)})({sp.latex(dv)})}}{{({sp.latex(v)})^2}}")

        # --- CASO B: PRODUCTO ---
        elif t.is_Mul and len([arg for arg in t.args if arg.has(x)]) > 1:
            st.warning("📐 **Técnica Detectada: Regla del Producto**")
            st.write("Se aplica la fórmula para el producto de dos funciones:")
            st.latex(r"\frac{d}{dx} [u \cdot v] = u' \cdot v + u \cdot v'")
            
            
            factores = [arg for arg in t.args if arg.has(x)]
            u, v = factores[0], sp.Mul(*factores[1:])
            du, dv = sp.diff(u, x), sp.diff(v, x)
            
            st.write("**Paso 1: Identificar componentes y sus derivadas:**")
            c1, c2 = st.columns(2)
            with c1:
                st.latex(f"u = {sp.latex(u)} \implies u' = {sp.latex(du)}")
            with c2:
                st.latex(f"v = {sp.latex(v)} \implies v' = {sp.latex(dv)}")
            
            st.write("**Paso 2: Sustituir en la fórmula:**")
            st.latex(f"({sp.latex(du)})({sp.latex(v)}) + ({sp.latex(u)})({sp.latex(dv)})")

        # --- CASO C: FORMAS GENERALIZADAS (SIN, COS, EXP) ---
        elif any(t.has(getattr(sp, n)) for n in ["sin", "cos", "exp"]):
            # Identificar cuál es
            if t.has(sp.sin):
                st.info("📐 **Fórmula Generalizada: Derivada del Seno**")
                st.latex(r"\frac{d}{dx} [\sin(ax)] = a \cdot \cos(ax)")
                
            elif t.has(sp.cos):
                st.info("📐 **Fórmula Generalizada: Derivada del Coseno**")
                st.latex(r"\frac{d}{dx} [\cos(ax)] = -a \cdot \sin(ax)")
            elif t.has(sp.exp):
                st.info("📐 **Fórmula Generalizada: Derivada Exponencial**")
                st.latex(r"\frac{d}{dx} [e^{ax}] = a \cdot e^{ax}")
                

            # Extraer argumento ax
            f_obj = [f for f in t.atoms(sp.Function) if f.func.__name__.lower() in ["sin", "cos", "exp"]]
            if not f_obj: f_obj = list(t.atoms(sp.exp))
            arg = f_obj[0].args[0]
            a = sp.diff(arg, x)
            
            st.write(f"Identificamos el coeficiente $a = {sp.latex(a)}$")
            st.write("**Resultado del término:**")
            st.latex(f"{sp.latex(sp.diff(t, x))}")

        # --- CASO D: POTENCIA ---
        else:
            st.info("📐 **Técnica: Regla de la Potencia Directa**")
            st.latex(r"\frac{d}{dx} [x^n] = n \cdot x^{n-1}")
            
            st.write("**Resultado del término:**")
            st.latex(f"{sp.latex(sp.diff(t, x))}")

        st.markdown("---")

    # --- CIERRE: RESULTADO FINAL ---
    st.success("### ✅ Resultado Final Simplificado")
    st.write("Uniendo y simplificando todos los pasos anteriores:")
    st.latex(f"f'(x) = {sp.latex(sp.simplify(sp.diff(h, x)))}")
